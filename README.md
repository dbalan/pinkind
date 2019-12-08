# pinkind

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
