from bs4 import BeautifulSoup
import requests
from playwright.sync_api import sync_playwright
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


# Standard headers to fetch a website
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/117.0.0.0 Safari/537.36"
}


def fetch_website_contents(url):
    """
    Return the title and contents of the website at the given url;
    truncate to 2,000 characters as a sensible limit
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    title = soup.title.string if soup.title else "No title found"
    if soup.body:
        for irrelevant in soup.body(["script", "style", "img", "input"]):
            irrelevant.decompose()
        text = soup.body.get_text(separator="\n", strip=True)
    else:
        text = ""
    return (title + "\n\n" + text)[:2_000]


def fetch_website_links(url):
    """
    Return the links on the webiste at the given url
    I realize this is inefficient as we're parsing twice! This is to keep the code in the lab simple.
    Feel free to use a class and optimize it!
    """
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, "html.parser")
    links = [link.get("href") for link in soup.find_all("a")]
    return [link for link in links if link]


def _scroll_to_bottom(page, max_scrolls=20, pause_ms=1000):
    """
    Scroll to the bottom of the page repeatedly so infinite-scroll / lazy-loaded
    content gets loaded. Stops when the page height stops growing, or after
    max_scrolls attempts (so endless feeds still return).
    """
    for _ in range(max_scrolls):
        prev_height = page.evaluate("document.body.scrollHeight")
        page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        page.wait_for_timeout(pause_ms)
        if page.evaluate("document.body.scrollHeight") == prev_height:
            break


def fetch_rendered_contents(url, max_chars=2_000, max_scrolls=20, scroll_pause_ms=1000):
    """
    Return the title and visible text of the website at the given url after
    JavaScript has run and infinite-scroll content has been loaded;
    truncate to max_chars characters.
    Uses Playwright's sync API, so call it from a regular script (not inside Jupyter).
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        try:
            page = browser.new_page(user_agent=headers["User-Agent"])
            page.goto(url, wait_until="domcontentloaded", timeout=30_000)
            try:
                page.wait_for_load_state("networkidle", timeout=10_000)
            except PlaywrightTimeoutError:
                pass  # pages with constant background traffic never go idle
            _scroll_to_bottom(page, max_scrolls, scroll_pause_ms)
            title = page.title() or "No title found"
            text = page.inner_text("body")
        finally:
            browser.close()
    return (title + "\n\n" + text)[:max_chars]
