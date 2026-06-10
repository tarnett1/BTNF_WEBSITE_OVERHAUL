import urllib.request
import re
import html
from html.parser import HTMLParser

class GoogleSitesParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.in_text_element = False
        self.paragraphs = []
        self.current_para = []
        self.image_urls = []
        
    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        # In Aristotle theme, text blocks are usually in spans with class C9DxTc
        if tag == 'span' and attrs_dict.get('class') == 'C9DxTc':
            self.in_text_element = True
        elif tag == 'img':
            src = attrs_dict.get('src', '')
            if src and ('googleusercontent.com' in src or 'logo.png' in src):
                self.image_urls.append(src)
                
    def handle_endtag(self, tag):
        if tag == 'span':
            self.in_text_element = False
            
    def handle_data(self, data):
        if self.in_text_element:
            text = data.strip()
            if text:
                self.current_para.append(text)
                
    def get_clean_paragraphs(self):
        # Join fragments and filter out boilerplate
        raw_paras = []
        # If we collect consecutive text, we can group them
        # However, for simplicity, let's just clean up what we collected
        text_content = " ".join(self.current_para)
        # Google Sites WIZ code wraps individual sentences or parts in spans,
        # so let's parse the text more smartly.
        return self.current_para

# Let's write a simpler parser that prints all text nodes inside body
class SimpleTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.recording = False
        self.text_blocks = []
        self.current_tag = None
        self.image_urls = []
        
    def handle_starttag(self, tag, attrs):
        self.current_tag = tag
        attrs_dict = dict(attrs)
        if tag in ('p', 'span', 'h1', 'h2', 'h3', 'h4', 'div'):
            # Check if it has a class that Google Sites uses for text
            cls = attrs_dict.get('class', '')
            if 'C9DxTc' in cls or 'zfr3Q' in cls or 'tyJCtd' in cls:
                self.recording = True
        if tag == 'img':
            src = attrs_dict.get('src', '')
            if src and 'googleusercontent.com' in src:
                self.image_urls.append(src)
                
    def handle_endtag(self, tag):
        if tag in ('p', 'span', 'h1', 'h2', 'h3', 'h4', 'div'):
            self.recording = False
            
    def handle_data(self, data):
        if self.recording:
            text = data.strip()
            if text and len(text) > 3:
                self.text_blocks.append(text)

with open("/Users/tarnett/.gemini/antigravity/brain/29b85260-ee2b-4105-844d-8291b040de43/.system_generated/steps/895/content.md", "r", encoding="utf-8") as f:
    html_content = f.read()

extractor = SimpleTextExtractor()
extractor.feed(html_content)

print("--- Extracted Text Blocks ---")
for idx, block in enumerate(extractor.text_blocks):
    print(f"[{idx}]: {block}")
    
print("\n--- Extracted Image URLs ---")
for idx, img in enumerate(extractor.image_urls):
    print(f"[{idx}]: {img}")
