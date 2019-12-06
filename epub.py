from ebooklib import epub
from newspaper import Article
import argparse


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
    article = Article(url)
    article.download()
    article.parse()

    title = article.title
    title_fn = title.lower().replace(' ', '-') 
    if len(title_fn) > 20:
        title_fn = title_fn[:20]
    
    c = epub.EpubHtml(title=title,
                   file_name=f'{title_fn}.xhtml',
                   lang='en')
    c.set_content(article.html)
    return c

def process_urls(links, outfile):
    parsed = list(map(get_article, links))
    build_book(parsed, outfile)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Builds epub of web articles")
    parser.add_argument("--outfile", default="output.epub", help="output file (default output.epub)")
    parser.add_argument("links", metavar="L", type=str, nargs="+", help="links to collect")

    args = parser.parse_args()

    outfile = args.outfile
    if not outfile.endswith(".epub"):
        outfile = f"{outfile}.epub"
    process_urls(args.links, outfile)
