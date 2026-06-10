import re

file_path = "/Users/tarnett/.gemini/antigravity/brain/29b85260-ee2b-4105-844d-8291b040de43/.system_generated/steps/605/content.md"

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Let's search for Casey or Goss (case-insensitive) in the entire content
matches = [m.start() for m in re.finditer(r'casey|goss', content, re.IGNORECASE)]

print(f"Found {len(matches)} matches for 'casey' or 'goss'")
for pos in matches:
    start = max(0, pos - 300)
    end = min(len(content), pos + 300)
    context = content[start:end]
    print(f"\nMatch at {pos}:")
    print(context)
