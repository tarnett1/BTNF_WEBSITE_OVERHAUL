import re

file_path = "/Users/tarnett/.gemini/antigravity/brain/29b85260-ee2b-4105-844d-8291b040de43/.system_generated/steps/605/content.md"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find all occurrences of lh3.googleusercontent.com/sitesv/
urls = re.findall(r'https://lh\d\.googleusercontent\.com/sitesv/[^\s"\'\\#&?]+(?:=w\d+)?', content)

print(f"Found {len(urls)} image URLs:")
for u in set(urls):
    print(u)
