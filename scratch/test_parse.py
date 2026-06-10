import urllib.request
import re
import html

url = "https://www.breakthroughsnf.com/counseling/amanda-king"
headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        content = response.read().decode('utf-8')
    
    print(f"Page size: {len(content)} bytes")
    
    # Check if keywords are in content
    keywords = ["Amanda", "King", "Yulee", "Florida", "counsel", "degree", "experience"]
    for kw in keywords:
        matches = [m.start() for m in re.finditer(kw, content, re.IGNORECASE)]
        print(f"Keyword '{kw}': found {len(matches)} matches")
        if matches:
            print(f"  First match context: {repr(content[max(0, matches[0]-100):min(len(content), matches[0]+100)])}")
            
except Exception as e:
    print(f"Error: {e}")
