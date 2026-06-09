import feedparser
import json
import re
from datetime import datetime
from collections import defaultdict

# RSS feed URLs
RSS_FEEDS = {
    "Deutsche Welle": "https://www.dw.com/en/rss",
    "BBC": "http://feeds.bbc.co.uk/news/rss.xml",
    "CNN": "http://rss.cnn.com/rss/edition.rss",
    "France24": "https://www.france24.com/en/rss"
}

# Keywords to filter by (easily editable)
KEYWORDS = ["technology", "climate", "politics", "war", "health"]

# Semantic associations for keywords. Articles matching these terms are treated as related to the keyword.
KEYWORD_ASSOCIATIONS = {
    "technology": [
        "tech",
        "software",
        "hardware",
        "artificial intelligence",
        "AI",
        "machine learning",
        "cybersecurity",
        "internet",
        "digital",
        "computing",
        "gadgets",
        "startup",
        "innovation"
    ],
    "climate": [
        "climate change",
        "global warming",
        "greenhouse",
        "emissions",
        "carbon",
        "sustainability",
        "environment",
        "ecology",
        "renewable",
        "sea level",
        "weather extremes"
    ],
    "politics": [
        "government",
        "election",
        "policy",
        "legislation",
        "parliament",
        "congress",
        "campaign",
        "diplomacy",
        "minister",
        "president",
        "senate",
        "political"
    ],
    "war": [
        "conflict",
        "battle",
        "military",
        "invasion",
        "troops",
        "army",
        "armed forces",
        "combat",
        "strike",
        "siege",
        "peace talks",
        "defense",
        "shelling"
    ],
    "health": [
        "medical",
        "hospital",
        "doctor",
        "nurse",
        "virus",
        "pandemic",
        "disease",
        "wellness",
        "healthcare",
        "nutrition",
        "mental health",
        "fitness"
    ]
}


def normalize_text(text):
    """Normalize text for consistent matching."""
    return (text or "").lower().strip()


def matches_keyword(keyword, text):
    """Check whether keyword text or its associations appear in the text."""
    text = normalize_text(text)
    if not text:
        return False

    if re.search(rf"\b{re.escape(keyword)}\b", text):
        return True

    for associated in KEYWORD_ASSOCIATIONS.get(keyword, []):
        if re.search(rf"\b{re.escape(associated)}\b", text):
            return True

    return False


def find_matching_keywords(title, summary):
    """Return all keywords that match the article title or summary."""
    matches = []

    for keyword in KEYWORDS:
        if matches_keyword(keyword, title) or matches_keyword(keyword, summary):
            matches.append(keyword)

    return matches


def fetch_news():
    """Fetch and filter news articles from RSS feeds."""
    articles_by_keyword = defaultdict(list)

    for source, url in RSS_FEEDS.items():
        try:
            feed = feedparser.parse(url)
            for entry in feed.entries[:10]:  # Limit to 10 articles per feed
                title = entry.get("title", "")
                summary = entry.get("summary", "")
                matched_keywords = find_matching_keywords(title, summary)

                for keyword in matched_keywords:
                    articles_by_keyword[keyword].append({
                        "source": source,
                        "title": title or "N/A",
                        "link": entry.get("link", "N/A"),
                        "published": entry.get("published", "N/A"),
                        "summary": summary[:200]
                    })
        except Exception as e:
            print(f"Error fetching from {source}: {e}")

    return articles_by_keyword

def generate_json_report():
    """Generate and save JSON report of filtered news."""
    articles = fetch_news()
    
    report = {
        "date": datetime.now().isoformat(),
        "sources": list(RSS_FEEDS.keys()),
        "keywords": KEYWORDS,
        "articles": dict(articles)
    }
    
    return json.dumps(report, indent=2)

if __name__ == "__main__":
    result = generate_json_report()
    print(result)
    
    # Optionally save to file
    with open("data/raw/news_report.json", "w") as f:
        f.write(result)