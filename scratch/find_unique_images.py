import json
import urllib.request
import re
import os
import html
from html.parser import HTMLParser

class ImageParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.image_urls = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'img':
            src = attrs_dict.get('src', '')
            if src and 'googleusercontent.com' in src:
                self.image_urls.append(src)

staff_paths = [
    "/counseling/amanda-king",
    "/counseling/aubrey-griffith",
    "/counseling/bethany-paige",
    "/counseling/bridget-hanlon",
    "/counseling/caitlin-rezac",
    "/counseling/devin-mcclure",
    "/counseling/hailey-dittenbir",
    "/counseling/jade-hebert",
    "/counseling/jason-kugel",
    "/counseling/jen-flores",
    "/counseling/jenny-savage",
    "/counseling/katelynn-schmidt",
    "/counseling/kelly-goss",
    "/counseling/marty-edwards",
    "/counseling/monica-hemming",
    "/counseling/nicki-peterson",
    "/counseling/peter-agdamag",
    "/counseling/roseline-shofolu",
    "/educational-staff/alex-beveridge",
    "/educational-staff/joanna-mcintosh",
    "/educational-staff/lizz-arnett",
    "/life-coaching/madison-moore",
    "/psychiatric-psychological-services/casey-goss"
]

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

# First, collect all image URLs for each path
url_map = {}
all_urls = []

for path in staff_paths:
    url = f"https://www.breakthroughsnf.com{path}"
    try:
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
        parser = ImageParser()
        parser.feed(content)
        
        # Clean up URLs
        cleaned_urls = []
        for img in parser.image_urls:
            img_clean = img.replace('\\/', '/').replace('\\', '')
            if 'logo.png' in img_clean:
                continue
            cleaned_urls.append(img_clean)
            all_urls.append(img_clean)
            
        url_map[path] = cleaned_urls
        print(f"Path {path}: found {len(cleaned_urls)} images.")
    except Exception as e:
        print(f"Error {path}: {e}")

# Count how many times each image URL appears across all pages
from collections import Counter
url_counts = Counter(all_urls)

print("\n--- Image Frequency Counts ---")
for url, count in url_counts.most_common(10):
    print(f"Count {count}: {url[:100]}...")

print("\n--- Unique Images For Each Page ---")
for path, urls in url_map.items():
    # Filter for URLs that appear only once in the entire crawl
    unique_urls = [u for u in urls if url_counts[u] == 1]
    print(f"\nPath: {path}")
    if unique_urls:
        for u in unique_urls:
            print(f"  UNIQUE: {u}")
    else:
        print("  NO UNIQUE IMAGE FOUND!")
