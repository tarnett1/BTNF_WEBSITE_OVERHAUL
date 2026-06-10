import re

file_path = "/Users/tarnett/.gemini/antigravity/brain/29b85260-ee2b-4105-844d-8291b040de43/.system_generated/steps/605/content.md"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Find all <img src="..."> tags
img_tags = re.findall(r'<img[^>]+src=["\']([^"\']+)["\'][^>]*>', content)

print("--- Image Tags Found ---")
for idx, src in enumerate(img_tags):
    print(f"{idx}: {src}")
