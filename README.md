# Pinkind

> Send your pinboard bookmarks / links to kindle


## Workdlow

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

Currently we use
[newspaper3k](https://newspaper.readthedocs.io/en/latest/) to parse
articles, I am not sure if there is a better library or API.

This code was inspired by [Kindlizer by
QuietMisdreavus](https://github.com/QuietMisdreavus/kindlizer)
