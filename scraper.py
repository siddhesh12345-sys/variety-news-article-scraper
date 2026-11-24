
import requests
import re
import csv
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from urllib.parse import urlparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime

WEBSITE_URL = "https://variety.com/"
WEBSITE_NAME = "Variety"
TIMEOUT = 15
MAX_WORKERS = 10

COLUMNS = [
    "Article Date",
    "Title",
    "URL",
    "Main Body Text",
    "Website Name"
]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120.0 Safari/537.36"
}

session = requests.Session()
session.headers.update(HEADERS)


def get_page(url):
    response = session.get(url, timeout=TIMEOUT)
    response.raise_for_status()
    return response.content


def get_sitemaps():
    response = session.get(
        WEBSITE_URL + "robots.txt",
        timeout=TIMEOUT
    )
    response.raise_for_status()

    urls = re.findall(
        r"(?im)^Sitemap:\s*(\S+)",
        response.text
    )

    if not urls:
        raise Exception("No sitemap found in robots.txt")

    return urls


def read_sitemap(url, visited=None, target_month=None):
    if visited is None:
        visited = set()

    if url in visited or len(visited) > 100:
        return []

    visited.add(url)
    results = []

    try:
        root = ET.fromstring(get_page(url))

        root_type = root.tag.split("}")[-1]

        if root_type == "sitemapindex":
            for sitemap in root:
                loc = ""
                for child in sitemap:
                    if child.tag.split("}")[-1] == "loc":
                        loc = child.text or ""

                if not loc:
                    continue

                # Only open child sitemaps matching the target month
                month_match = re.search(
                    r"(20\d{2})[-_]?(\d{2})",
                    loc
                )

                if month_match:
                    month = month_match.group(1) + "-" + month_match.group(2)

                    if month != target_month:
                        continue

                results.extend(
                    read_sitemap(
                        loc,
                        visited,
                        target_month
                    )
                )

        elif root_type == "urlset":
            for item in root:
                data = {}

                for child in item:
                    tag = child.tag.split("}")[-1]
                    data[tag] = child.text or ""

                article_url = data.get("loc", "")
                lastmod = data.get("lastmod", "")

                if article_url and "variety.com" in urlparse(article_url).netloc:
                    results.append({
                        "url": article_url,
                        "lastmod": lastmod
                    })

    except Exception as error:
        print("Sitemap error:", url, error)

    return results


def extract_article(article_url):
    try:
        response = session.get(
            article_url,
            timeout=TIMEOUT
        )
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        # Title
        title = ""

        h1 = soup.find("h1")
        if h1:
            title = h1.get_text(" ", strip=True)

        if not title:
            tag = soup.find("meta", property="og:title")
            if tag:
                title = tag.get("content", "")

        # Publication date
        date = ""

        date_tags = [
            soup.find("meta", property="article:published_time"),
            soup.find("meta", attrs={"name": "date"}),
            soup.find("time", attrs={"datetime": True})
        ]

        for tag in date_tags:
            if tag:
                value = (
                    tag.get("content")
                    or tag.get("datetime")
                    or tag.get_text(strip=True)
                )

                match = re.search(r"\d{4}-\d{2}-\d{2}", value)

                if match:
                    date = match.group(0)
                    break

        # Main body
        article = soup.find("article")
        if article:
            paragraphs = article.find_all("p")
        else:
            main = soup.find("main")
            paragraphs = main.find_all("p") if main else []

        body = "\n\n".join(
            p.get_text(" ", strip=True)
            for p in paragraphs
            if len(p.get_text(strip=True)) > 30
        )

        if not title or not date:
            return None

        return {
            "Article Date": date,
            "Title": title,
            "URL": article_url,
            "Main Body Text": body,
            "Website Name": WEBSITE_NAME
        }

    except Exception as error:
        print("Article error:", article_url, error)
        return None


def search_articles(target_date, progress_callback=None):

    datetime.strptime(target_date, "%Y-%m-%d")
    target_month = target_date[:7]

    print("Searching for:", target_date)

    # Step 1: Find relevant sitemap entries
    sitemap_urls = get_sitemaps()
    sitemap_entries = []

    for sitemap in sitemap_urls:
        sitemap_entries.extend(
            read_sitemap(
                sitemap,
                target_month=target_month
            )
        )

    # Step 2: Filter using lastmod as a preliminary hint only.
    # Lastmod is NOT proof of publication date, so entries without
    # matching lastmod are retained to avoid missing articles.
    candidates = []

    for item in sitemap_entries:
        lastmod = item["lastmod"][:10]

        if lastmod == target_date or not lastmod:
            candidates.append(item["url"])

    candidates = list(dict.fromkeys(candidates))

    print("Candidate articles:", len(candidates))

    if not candidates:
        return []

    # Step 3: Download article pages concurrently
    articles = []
    completed = 0
    total = len(candidates)

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        futures = {
            executor.submit(extract_article, url): url
            for url in candidates
        }

        for future in as_completed(futures):
            completed += 1

            try:
                article = future.result()

                if article and article["Article Date"] == target_date:
                    if article["Main Body Text"]:
                        articles.append(article)

            except Exception as error:
                print("Error:", error)

            if progress_callback:
                progress_callback(
                    completed,
                    total,
                    f"Checking articles: {completed}/{total}"
                )

    # Step 4: Save results
    articles.sort(key=lambda x: x["Title"].lower())

    with open(
        "articles.csv",
        "w",
        newline="",
        encoding="utf-8-sig"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=COLUMNS)
        writer.writeheader()
        writer.writerows(articles)

    print("Articles found:", len(articles))

    return articles
