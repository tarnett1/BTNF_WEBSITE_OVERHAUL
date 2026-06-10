import urllib.request
import os

os.makedirs("images", exist_ok=True)

urls = {
    "marty.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUAQDl-0C1tZUxCxUqIo5Hz23GALTvSHnuCtWNVAjfQFCte7Or1eAIAIyJokf7Sc3npC2aX468CiViRlSB-cMie-krGR6PrxjahrobtIP_BKg-tX-mNcede2FRqBWAUq9lZDf6lvVfD0AIjI9s1FcxBXiMJ9h-E4g9N_Ni_DVc9NVWyI4HuLV_wVyFH1LVoG9tMwDdHgIj7UaUXxSA4=w1280",
    "lizz.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUCaMbcW9xNe75uRDtTK0XuMgOb0aykpYsKGq0hgPMvStNLH9EF9wbZ-O0cuWir9UYXpRlPSTW9NxOa8SbV8HMAEfwUnKFQrgn7y9txtxzKlly9auTk5WRueq2ryNrJSKBsX-a2TAT5QiqN3QgYDbD8WRMx3kebEQgwni7j36P1haS7pvVvFhCFeFyrWgyECaQlKI_go9GxXHX6aOzfB0Q0TGP0CMxm6xoTdZIQsa4A=w1280",
    "casey.jpg": "https://lh3.googleusercontent.com/sitesv/AA5AbUC97ep6MgZzwJtD1wOo3-9JWLIkQ5EMCtmB1uoo2_NBf1mmx7JA2EZN4LQ5mfLuWwTZQCja7mlvwSZRgRLNFahgRcW4lBr6u_UYLmr1AQaRZi658IwxGJRJKFi_ttW2Qcskzn6k4qzgyvN38JmUTWtgtNLjcL_4BXnP2gX6qPe6PhVY1fQS8q3-oMWROi9ZkaiGe6ttZuL-471vlWw1srL0goKeOmy4AzErhRnG=w1280"
}

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Referer': 'https://www.breakthroughsnf.com/our-staff'
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
