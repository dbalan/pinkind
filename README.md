# Pinkind

> Send your pinboard bookmarks / links to kindle


[![builds.sr.ht status](https://builds.sr.ht/~dbalan/pinkind/freebsd.yml.svg)](https://builds.sr.ht/~dbalan/pinkind/freebsd.yml?)


## Workflow

As the title says the code was written to send articles to my
kindle. Pinkindle generates epub's but kindle can't read epub -- so
how does it work?

I use following workflow to get around this.

1. Use pinkindle to generate `epub`
2. Use `ebook-convert` from [Calibre](https://calibre-ebook.com/) to convert it into `.mobi` file.
3. Email it to kindle ebook sync service (whatever it is called)

## Usage

Pinkind takes web article links, downloads them and builds epub out of
the article.

```bash
python epub.py links https://en.wikipedia.org/wiki/Uncanny_valley  \
	https://www.theatlantic.com/magazine/archive/1945/07/as-we-may-think/303881/
```

Pinkind can also get links direct from a pinboard account. In that
case provide API key and tag to filter out links.

```bash
python epub.py pinboard --tag kindle <API_KEY>
```

## Todo

Article formatting is still hit or miss. Currently we use
[newspaper3k](https://newspaper.readthedocs.io/en/latest/) to parse
articles, try using [Mercury parser](https://mercury.postlight.com/web-parser/).

## Thanks

Started thinking about this after seeing [Kindlizer by
QuietMisdreavus](https://github.com/QuietMisdreavus/kindlizer)
