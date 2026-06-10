import urllib.request
import os
import re
import json
import html
from html.parser import HTMLParser
from collections import Counter

os.makedirs("images", exist_ok=True)
os.makedirs("scratch/data", exist_ok=True)

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

class SitesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.recording = False
        self.text_blocks = []
        self.image_urls = []
        self.page_title = ""
        self.in_title = False
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'title':
            self.in_title = True
        elif tag in ('p', 'span', 'h1', 'h2', 'h3', 'h4', 'div'):
            cls = attrs_dict.get('class', '')
            if 'C9DxTc' in cls or 'zfr3Q' in cls or 'tyJCtd' in cls:
                self.recording = True
        elif tag == 'img':
            src = attrs_dict.get('src', '')
            if src and 'googleusercontent.com' in src:
                self.image_urls.append(src)
                
    def handle_endtag(self, tag):
        if tag == 'title':
            self.in_title = False
        elif tag in ('p', 'span', 'h1', 'h2', 'h3', 'h4', 'div'):
            self.recording = False
            
    def handle_data(self, data):
        if self.in_title:
            self.page_title += data
        elif self.recording:
            text = data.strip()
            if text and len(text) > 3:
                self.text_blocks.append(text)

def clean_text_blocks(blocks):
    clean = []
    seen = set()
    boilerplate = [
        "Find Us & Like Us on Facebook",
        "Now Accepting United Healthcare",
        "BREAKTHROUGHS IS AN APPROVED PROVIDER",
        "FAMILY EMPOWERMENT SCHOLARSHIP",
        "Click Here for More Info",
        "904-849-1190",
        "Yulee, Florida 32097",
        "office@breakthroughsnf.com",
        "is NOT Lindamood-Bell",
        "is NOT affiliated with",
        "in no way endorses or monitors",
        "Breakthroughs of North Florida"
    ]
    for b in blocks:
        b_clean = html.unescape(b).strip()
        b_clean = re.sub(r'\s+', ' ', b_clean)
        # Skip if too short
        if len(b_clean) < 5:
            continue
        if any(bp in b_clean for bp in boilerplate):
            continue
        # Skip duplicates
        if b_clean.lower() in seen:
            continue
        seen.add(b_clean.lower())
        clean.append(b_clean)
    return clean

def scrape_page(path):
    url = f"https://www.breakthroughsnf.com{path}"
    try:
        print(f"Scraping {url}...")
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req) as response:
            content = response.read().decode('utf-8')
            
        parser = SitesParser()
        parser.feed(content)
        
        clean_text = clean_text_blocks(parser.text_blocks)
        
        cleaned_images = []
        for img in parser.image_urls:
            img_clean = img.replace('\\/', '/').replace('\\', '')
            if 'logo.png' in img_clean:
                continue
            cleaned_images.append(img_clean)
                
        return {
            "title": parser.page_title.replace("Breakthroughs of North Florida - ", "").strip(),
            "text": clean_text,
            "images": cleaned_images
        }
    except Exception as e:
        print(f"Error scraping {url}: {e}")
        return None

def download_image(url, local_name):
    filepath = os.path.join("images", local_name)
    try:
        if os.path.exists(filepath) and os.path.getsize(filepath) > 0:
            print(f"Image {local_name} already exists. Skipping.")
            return filepath
            
        print(f"Downloading image to {filepath}...")
        req = urllib.request.Request(url, headers=HEADERS)
        with urllib.request.urlopen(req) as response:
            data = response.read()
        with open(filepath, "wb") as f:
            f.write(data)
        print(f"Successfully saved {local_name} ({len(data)} bytes)")
        return filepath
    except Exception as e:
        print(f"Failed to download image {url}: {e}")
        return None

def main():
    staff_paths = [
        "/counseling/amanda-king",
        "/counseling/aubrey-griffith",
        "/counseling/bethany-paige",
        "/counseling/bridget-hanlon",
        "/counseling/caitlin-rezac",
        "/counseling/devin-mcclure",
        "/counseling/hailey-dittenbir",
        "/counseling/jade-hebert",
        "/counseling/jason-kugel",
        "/counseling/jen-flores",
        "/counseling/jenny-savage",
        "/counseling/katelynn-schmidt",
        "/counseling/kelly-goss",
        "/counseling/marty-edwards",
        "/counseling/monica-hemming",
        "/counseling/nicki-peterson",
        "/counseling/peter-agdamag",
        "/counseling/roseline-shofolu",
        "/educational-staff/alex-beveridge",
        "/educational-staff/joanna-mcintosh",
        "/educational-staff/lizz-arnett",
        "/life-coaching/madison-moore",
        "/psychiatric-psychological-services/casey-goss"
    ]
    
    program_paths = [
        "/programs/barton",
        "/programs/lindamood-bell",
        "/programs/lindamood-bell/lips",
        "/programs/lindamood-bell/on-cloud-9",
        "/programs/lindamood-bell/seeing-stars",
        "/programs/lindamood-bell/talkies",
        "/programs/lindamood-bell/visualizing-verbalizing",
        "/programs/love-and-logic",
        "/programs/satact-test-prep",
        "/tutoring"
    ]
    
    other_paths = [
        "/insurance",
        "/forms",
        "/privacy-policy"
    ]
    
    # 1. Scrape all staff pages first and collect image URLs
    staff_raw = {}
    all_images = []
    
    for path in staff_paths:
        data = scrape_page(path)
        if data:
            staff_raw[path] = data
            all_images.extend(data["images"])
            
    # 2. Count image frequency to find unique ones
    image_counts = Counter(all_images)
    
    # 3. Process staff profiles and download unique pictures
    staff_data = []
    for path, data in staff_raw.items():
        name_key = path.split("/")[-1]
        name = data["title"].split("-")[0].strip()
        
        # Heuristic: Find first unique image, otherwise fallback to first image in list
        unique_images = [img for img in data["images"] if image_counts[img] == 1]
        
        # Download image
        profile_pic = ""
        # If Marty, Lizz, or Casey, they already have correct local files from earlier
        if name_key == "marty-edwards":
            profile_pic = "images/marty.jpg"
        elif name_key == "lizz-arnett":
            profile_pic = "images/lizz.jpg"
        elif name_key == "casey-goss":
            profile_pic = "images/casey.jpg"
        else:
            if unique_images:
                # Use the first unique image
                target_img_url = unique_images[0]
            elif data["images"]:
                # Use first available image
                target_img_url = data["images"][0]
            else:
                target_img_url = None
                
            if target_img_url:
                img_name = f"{name_key.replace('-', '_')}.jpg"
                downloaded = download_image(target_img_url, img_name)
                if downloaded:
                    profile_pic = downloaded
            else:
                profile_pic = "images/default_avatar.jpg"
                
        # Smart classification of text blocks
        role = "Specialist"
        education_blocks = []
        bio_blocks = []
        
        # Skip name block if it is the first block
        text_blocks = data["text"]
        if text_blocks and text_blocks[0].lower() in (name.lower(), name_key.replace('-', ' ').lower()):
            text_blocks = text_blocks[1:]
            
        # Identify role (usually next block)
        if text_blocks:
            first_block = text_blocks[0]
            if len(first_block) < 100 or "Therapist" in first_block or "Intern" in block or "Specialist" in block or "LMHC" in block or "LCSW" in block or "Psychiatric" in block or "Nurse" in block or "Life Coach" in block:
                role = first_block
                text_blocks = text_blocks[1:]
                
        for block in text_blocks:
            # Check if it looks like education info
            is_edu = any(w in block.lower() for w in ["degree", "university", "bachelor", "master", "ph.d", "graduate", "college", "studied"])
            # But ignore if it's too long (probably bio paragraph that mentions their degree)
            if is_edu and len(block) < 250:
                education_blocks.append(block)
            else:
                bio_blocks.append(block)
                
        education = " ".join(education_blocks)
        bio = "\n\n".join(bio_blocks)
        
        # Ensure "Michelle" is not in any field
        role = role.replace("Michelle", "").replace("  ", " ").strip()
        education = education.replace("Michelle", "").replace("  ", " ").strip()
        bio = bio.replace("Michelle", "").replace("  ", " ").strip()
        
        staff_data.append({
            "key": name_key,
            "name": name,
            "role": role,
            "education": education,
            "bio": bio,
            "image": profile_pic,
            "category": "counseling" if "counseling" in path else "education" if "educational" in path else "psychiatric" if "psychiatric" in path else "coaching"
        })
        
    with open("scratch/data/staff.json", "w") as f:
        json.dump(staff_data, f, indent=2)
        
    # 4. Process programs
    program_data = []
    for path in program_paths:
        data = scrape_page(path)
        if data:
            clean_blocks = [b.replace("Michelle", "") for b in data["text"]]
            program_data.append({
                "key": path.split("/")[-1],
                "title": data["title"].replace("Michelle", ""),
                "text": "\n\n".join(clean_blocks)
            })
            
    with open("scratch/data/programs.json", "w") as f:
        json.dump(program_data, f, indent=2)
        
    # 5. Process other pages (insurance, forms, privacy)
    other_data = {}
    for path in other_paths:
        data = scrape_page(path)
        if data:
            clean_blocks = [b.replace("Michelle", "") for b in data["text"]]
            other_data[path.split("/")[-1]] = {
                "title": data["title"].replace("Michelle", ""),
                "text": "\n\n".join(clean_blocks)
            }
            
    with open("scratch/data/other.json", "w") as f:
        json.dump(other_data, f, indent=2)
        
    print("Cleaned migration data generated successfully!")

if __name__ == "__main__":
    main()
