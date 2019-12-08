from ebooklib import epub
from newspaper import Article, article
import argparse
import logging
import pinboard
import datetime
import sys

log = logging.getLogger(__name__)

def build_book(articles, filename):
    book = epub.EpubBook()
    book.set_identifier("pinkindbook")
    book.set_title('Pinkind Article Collection')
    book.set_language('en')
    book.add_author('pinkind.dbalan.in')

    style = 'body { font-family: Times, Times New Roman, serif; }'
    nav_css = epub.EpubItem(uid="style_nav",
                            file_name="style/nav.css",
                            media_type="text/css",
                            content=style)

    nav_css = epub.EpubItem(uid="style_nav",
                        file_name="style/nav.css",
                        media_type="text/css",
                        content=style)
    book.add_item(nav_css)

    spine = []
    for art in articles:
        book.add_item(art)
        spine.append(art)
        
    book.toc = spine
    
    book.spine = ['nav'] + spine
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())
    epub.write_epub(filename, book)
    
def get_article(url):
    try:
        article = Article(url)
        article.download()
        article.parse()
    except Exception:
        log.warn(f"execeptiopn {url}")
        return None
    title = article.title

    if not title:
        # skip the article
        log.warn(f"skipping article: {url}")
        return None
    
    title_fn = title.lower().replace(' ', '-') 
    if len(title_fn) > 20:
        title_fn = title_fn[:20]

    c = epub.EpubHtml(title=title,
                   file_name=f'{title_fn}.xhtml',
                   lang='en')
    if not article.text:
        return None
    c.set_content(article.html)
        
    return c

def process_urls(links, outfile):
    parsed = list(filter(bool, map(get_article, links)))
    if not parsed:
        log.warn("empyt")
        return 
    build_book(parsed, outfile)

def get_recent_unread(api_key, tags=["kindle"]):
    pb = pinboard.Pinboard(api_key)
    bookmarks = pb.posts.recent(count=50, tag=tags)

    posts = []
    for bm in bookmarks.get('posts'):
        if bm.toread:
            posts.append(bm.url)
    return posts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Builds epub of web articles")
    parser.add_argument("--outfile", default="output.epub", help="output file (default output.epub)")

    subparsers = parser.add_subparsers()
    p_links = subparsers.add_parser("links")
    p_pinboard = subparsers.add_parser("pinboard")
    
    p_links.add_argument("links", type=str, nargs="+", help="links to collect")

    p_pinboard.add_argument("api", type=str, help="pinboard api key")
    p_pinboard.add_argument("--tag", type=str, help="tags to filter")
    args = parser.parse_args()

    if 'api' in args:
        links = get_recent_unread(args.api, tags=[args.tag])
    elif 'links' in args:
        links = args.links
    else:
        parser.print_help()
        sys.exit(-1)

    if not args.outfile.endswith(".epub"):
        outfile = f'{args.outfile}.epub'
    else:
        outfile = args.outfile
    process_urls(links, outfile)
    log.info(f"output file written to : {outfile}")
