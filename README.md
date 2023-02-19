# lim

## About

An simple [textboard](https://en.wikipedia.org/wiki/Textboard) made as a
simple version of my currently definitely not abandoned infinitely large
textboard [inf](https://github.com/gscbravo/inf). Currently, I'm going to
be working on this for right now as to work on porting it to
[SQLite](https://en.wikipedia.org/wiki/SQLite) for better data management.

Currently, no registration is required to comment on the forum. Posts are
stored in SQLite. Each comment is assigned a comment number to uniquely
identify it.

The defaults for the forum are found in variables at the top of `app.py`.

### Defaults
- Maximum number of comments per board: `1000`
- Maximum comment length: `2000`
- Post name: `Guest`
- Site name: `Limited Forums`
- Site description: `Limited Forums open comments section`

## Usage

```
pip3 install -r requirements.txt
cd src
flask run
```

When in production, use a WSGI server such as [Gunicorn](https://gunicorn.org/)
with [Nginx](https://nginx.org/).

## TODO

- [ ] Make sure this works with multiple threads and processes as workers
- [ ] Replies
- [ ] Config file to configure settings
- [ ] Website admin area to configure settings
- [ ] Tripcodes
- [ ] Image upload
- [ ] Moderation of comments
