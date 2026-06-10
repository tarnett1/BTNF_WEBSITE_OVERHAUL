import re

file_path = "/Users/tarnett/.gemini/antigravity/brain/29b85260-ee2b-4105-844d-8291b040de43/.system_generated/steps/605/content.md"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find all occurrences of Casey Goss
matches = [m.start() for m in re.finditer(r'Casey Goss', content)]

for idx, pos in enumerate(matches):
    print(f"\n--- Casey Goss Match {idx} at {pos} ---")
    # Search backwards for lh3.googleusercontent.com
    # Let's search in content[pos-3000:pos]
    sub = content[max(0, pos-3000):pos]
    urls = re.findall(r'https?:\\?/\\?/[a-zA-Z0-9_-]+\.googleusercontent\.com\\?/sitesv\\?/[^"\'\s\\#&?]+(?:=w\d+)?', sub)
    if urls:
        print("Found image URLs before Casey Goss:")
        for u in urls:
            print(u.replace('\\/', '/').replace('\\', ''))
    else:
        print("No image URLs found in the preceding 3000 chars.")
