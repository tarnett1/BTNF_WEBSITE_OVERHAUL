import os
import urllib.request

# Ensure the images directory exists
os.makedirs("images", exist_ok=True)

# Define the logo targets with their URLs and clean SVG fallbacks
LOGOS = {
    "bcbs_logo.svg": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/8f/Blue_Cross_and_Blue_Shield_Association_logo.svg",
        "fallback": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100" width="100%" height="100%">
  <rect width="100%" height="100%" fill="none"/>
  <!-- Blue Cross Symbol -->
  <path d="M 40,25 h 20 v -20 h 20 v 20 h 20 v 20 h -20 v 20 h -20 v -20 h -20 z" fill="#005691"/>
  <!-- Blue Shield Outline -->
  <path d="M 35,15 L 70,5 L 105,15 L 105,45 C 105,70 70,90 70,90 C 70,90 35,70 35,45 Z" fill="none" stroke="#005691" stroke-width="4"/>
  <!-- Text -->
  <text x="125" y="58" font-family="'Plus Jakarta Sans', sans-serif" font-size="28" font-weight="800" fill="#002d62">Florida Blue</text>
  <text x="125" y="80" font-family="'Inter', sans-serif" font-size="14" font-weight="600" fill="#718096" letter-spacing="1">CROSS &amp; SHIELD</text>
</svg>"""
    },
    "uhc_logo.svg": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/85/UnitedHealthcare_Logo.svg",
        "fallback": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100" width="100%" height="100%">
  <rect width="100%" height="100%" fill="none"/>
  <!-- UHC "U" Logo Mark -->
  <path d="M 30,15 H 65 V 55 C 65,70 50,85 30,85 C 10,85 0,70 0,55 Z" fill="#00263e" transform="translate(35, 0)"/>
  <path d="M 12,15 H 23 V 55 C 23,65 17,73 12,73 Z" fill="#e87722" transform="translate(35, 0)"/>
  <!-- Text -->
  <text x="125" y="58" font-family="'Plus Jakarta Sans', sans-serif" font-size="26" font-weight="800" fill="#00263e">UnitedHealthcare</text>
</svg>"""
    },
    "aetna_logo.svg": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/8/82/Aetna_logo.svg",
        "fallback": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100" width="100%" height="100%">
  <rect width="100%" height="100%" fill="none"/>
  <!-- Aetna Wordmark and Heart style logo -->
  <text x="40" y="65" font-family="'Plus Jakarta Sans', sans-serif" font-size="48" font-weight="800" fill="#7b1fa2" letter-spacing="-2">aetna</text>
  <!-- Heart graphic next to it -->
  <path d="M 180,45 C 180,35 190,25 200,25 C 210,25 220,35 220,45 C 220,60 180,80 180,80 C 180,80 140,60 140,45 C 140,35 150,25 160,25 C 170,25 180,35 180,45 Z" fill="#7b1fa2" transform="translate(15, 0)"/>
</svg>"""
    },
    "cigna_logo.svg": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/3d/Cigna_logo_2021.svg",
        "fallback": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100" width="100%" height="100%">
  <rect width="100%" height="100%" fill="none"/>
  <!-- Cigna Tree-person Symbol -->
  <circle cx="60" cy="30" r="10" fill="#09805d"/>
  <path d="M 40,75 C 40,60 50,45 60,45 C 70,45 80,60 80,75 Z" fill="#024835"/>
  <path d="M 60,45 L 85,30 M 60,55 L 35,45" stroke="#09805d" stroke-width="6" stroke-linecap="round"/>
  <!-- Text -->
  <text x="125" y="62" font-family="'Plus Jakarta Sans', sans-serif" font-size="36" font-weight="800" fill="#024835" letter-spacing="-1">Cigna</text>
</svg>"""
    },
    "tricare_logo.svg": {
        "url": "https://upload.wikimedia.org/wikipedia/commons/3/36/US-TRICARE-Logo.svg",
        "fallback": """<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100" width="100%" height="100%">
  <rect width="100%" height="100%" fill="none"/>
  <!-- Tricare Shield / Ribbon style -->
  <path d="M 35,20 H 95 V 50 C 95,70 65,85 65,85 C 65,85 35,70 35,50 Z" fill="#0a2540"/>
  <path d="M 45,28 H 85 V 48 C 85,62 65,73 65,73 C 65,73 45,62 45,48 Z" fill="#d9232a"/>
  <polygon points="65,33 69,42 79,42 71,47 74,57 65,51 56,57 59,47 51,42 61,42" fill="#ffffff"/>
  <!-- Text -->
  <text x="125" y="58" font-family="'Plus Jakarta Sans', sans-serif" font-size="32" font-weight="800" fill="#0a2540" letter-spacing="1">TRICARE</text>
  <text x="125" y="78" font-family="'Inter', sans-serif" font-size="12" font-weight="700" fill="#d9232a" letter-spacing="2">MILITARY HEALTH</text>
</svg>"""
    }
}

headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

def download_logo(filename, data):
    filepath = os.path.join("images", filename)
    print(f"Fetching {filename}...")
    try:
        req = urllib.request.Request(data["url"], headers=headers)
        with urllib.request.urlopen(req, timeout=5) as response:
            with open(filepath, "wb") as f:
                f.write(response.read())
        print(f"✅ Downloaded {filename} successfully!")
    except Exception as e:
        print(f"⚠️ Failed to download {filename} from remote ({e}). Using local high-quality vector fallback.")
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(data["fallback"])
        print(f"✅ Generated fallback {filename}!")

def main():
    for name, info in LOGOS.items():
        download_logo(name, info)

if __name__ == "__main__":
    main()
