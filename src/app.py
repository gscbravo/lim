# app.py - main program
# Copyright (C) 2022  GSC Bravo

# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.

from datetime import datetime, timezone
from flask import Flask, render_template, redirect, request
import sqlite3

# max number of comments to store
MAX_COMMENTS = 1000
# max chars in comment
MAX_COMMENT_LENGTH = 2000
# default name
DEFAULT_NAME = 'Guest'
# site name
SITE_NAME = 'Limited Forums'
# site description
SITE_DESCRIPTION = 'Limited Forums open comments section'

app = Flask(__name__)

# initialize database if doesn't exist
def db_init():
    conn = sqlite3.connect('board.db')
    cur = conn.cursor()
    cur.execute('''create table if not exists posts (
            name text,
            subject text,
            text text,
            date text
            )''')
    conn.commit()

db_init()

@app.route('/')
def load_board():
    conn = sqlite3.connect('board.db')
    cur = conn.cursor()
    res = cur.execute('select rowid, * from posts').fetchall()
    board_comments = []
    for comment in res:
        board_comments.insert(0, [comment[0], comment[1], comment[2], comment[3].split('\n'), comment[4]])
    return render_template('comments.html', comments=board_comments, default_name=DEFAULT_NAME, site_name=SITE_NAME, site_description=SITE_DESCRIPTION)

@app.route('/submit', methods=['GET', 'POST'])
def submit():
    if request.method == 'GET':
        return redirect('/')
    # get form args name, subject, text
    # only text is going to be actually required to post
    name = request.form.get('name', '').strip()
    subject = request.form.get('subject', '').strip()
    text = request.form.get('text', '').strip()

    # if text is empty, error
    if not text:
        return render_template('error.html', error='Text box must not be empty')

    # limit comment length
    if len(text) > MAX_COMMENT_LENGTH:
        return render_template('error.html', error=f'Text must be no more than {MAX_COMMENT_LENGTH} characters')

    # if name is empty, set to default name
    if not name:
        name = DEFAULT_NAME

    # insert comment and return to post sent
    comment_data = (
        name,
        subject,
        text,
        str(datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S'))
        )

    conn = sqlite3.connect('board.db')
    cur = conn.cursor()

    # drop oldest post if at limit
    if len(cur.execute('select * from posts').fetchall()) >= MAX_COMMENTS:
        cur.execute('delete from posts where rowid in (select rowid from posts limit 1)')

    cur.execute('insert into posts values (?, ?, ?, ?)', comment_data)
    conn.commit()

    return redirect('/')

if __name__ == '__main__':
    app.run()
