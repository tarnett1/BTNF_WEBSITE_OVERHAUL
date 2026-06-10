import re

file_path = "/Users/tarnett/.gemini/antigravity/brain/29b85260-ee2b-4105-844d-8291b040de43/.system_generated/steps/605/content.md"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find all href="..." patterns
hrefs = re.findall(r'href=["\']([^"\']+)["\']', content)

links = set()
for href in hrefs:
    # We want internal links (either relative starting with / or absolute pointing to breakthroughsnf.com)
    # Exclude external links and static resources
    if (href.startswith("/") and not href.startswith("//")) or "breakthroughsnf.com" in href:
        clean_href = href.split("?")[0].split("#")[0]
        # Ignore empty or slash-only links
        if clean_href and clean_href != "/":
            links.add(clean_href)

print("--- Unique Internal Links Found ---")
for link in sorted(list(links)):
    print(link)
