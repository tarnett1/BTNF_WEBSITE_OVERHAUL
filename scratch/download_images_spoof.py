import urllib.request
import os

os.makedirs("images", exist_ok=True)

urls = {
    "marty.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUDxtmqfG5c35LlWSsuprte5KQZPAMAne0UOUaOBq1RWbdZhgXV17hDvLSaZO-YHVcOnVKLKvyogyxQXvEobpcsoD2udBDdJmA3499BRGOFGStgTNi2fVsrx9YNdi-a_BdRs0KdoUqNkbWWX1-qCsOmMo5Td8gyplJo2BkcWDyjqKnZ4i-b4sVZzb5hlUHUmS7V6EZXTq1d0LqmNt630fzkvCBU8DNjTCIKWF7OSm_s=w1280",
    "lizz.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUB4LAHwD1Lv4owAeoLgWZlgLBT9qlyHh9FAhhULLD6UOmBcVzkLr2nlN0Cq2Av4MGm4KPD-GAuRKLhsbnKeNBo2t_UR3epk0yGnPeabKa6rX6qTl8RD39RF3QJx209O7YmQNRBPWcCy8S3EMJLSug_LFlDflQH_Ox7cXzOwW5H3tpJNUYQN7WYN6lKlRwvg33CIk0CzmGeTCR4UryS3vx7d_Wl9ADJ6J2KhcgYHcrE=w1280",
    "casey.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUChhLulc14JldZFpdiusmN-zmpJf05GiezhN_-_DGdAfHW2S8twVPq1d0sVbhhEcgNEodtmfBkVekRyRQpsFT8WcEeCgBzdF__3ew0iamO9aszDxt5ECgeYnjxHmcGWiTE4UW9fRm4CSZ9iO5rSRAqr9pVg0XLbCQ3kiUIu8DUHg_czK6UqSIt7Wuz58ZlaibHvf2we7qILqs2DpILNPnchIdGPNSHiJSJQDZXn=w1280"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.breakthroughsnf.com/'
}

for filename, url in urls.items():
    try:
        print(f"Downloading {filename}...")
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req) as response:
            data = response.read()
            filepath = os.path.join("images", filename)
            with open(filepath, "wb") as f:
                f.write(data)
            print(f"Successfully saved {filepath} ({len(data)} bytes)")
    except Exception as e:
        print(f"Failed to download {filename}: {e}")
