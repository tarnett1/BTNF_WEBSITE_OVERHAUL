import urllib.request
import os

os.makedirs("images", exist_ok=True)

url = "https://lh3.googleusercontent.com/sitesv/AA5AbUDxtmqfG5c35LlWSsuprte5KQZPAMAne0UOUaOBq1RWbdZhgXV17hDvLSaZO-YHVcOnVKLKvyogyxQXvEobpcsoD2udBDdJmA3499BRGOFGStgTNi2fVsrx9YNdi-a_BdRs0KdoUqNkbWWX1-qCsOmMo5Td8gyplJo2BkcWDyjqKnZ4i-b4sVZzb5hlUHUmS7V6EZXTq1d0LqmNt630fzkvCBU8DNjTCIKWF7OSm_s=w1280"

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Accept': 'image/avif,image/webp,image/apng,image/svg+xml,image/*,*/*;q=0.8',
    'Accept-Language': 'en-US,en;q=0.9',
    'Sec-Fetch-Dest': 'image',
    'Sec-Fetch-Mode': 'no-cors',
    'Sec-Fetch-Site': 'cross-origin'
}

try:
    print("Downloading marty.jpg with advanced headers...")
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as response:
        data = response.read()
        filepath = os.path.join("images", "marty.jpg")
        with open(filepath, "wb") as f:
            f.write(data)
        print(f"Successfully saved {filepath} ({len(data)} bytes)")
except Exception as e:
    print(f"Failed: {e}")
