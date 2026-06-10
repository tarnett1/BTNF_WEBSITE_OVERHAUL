import os
import sys
from html.parser import HTMLParser

class HTMLValidator(HTMLParser):
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.tags_stack = []
        self.errors = []
        self.has_skip_link = False
        self.has_main = False
        self.has_header = False
        self.has_footer = False
        self.has_style = False
        self.labels = set()
        self.inputs = set()
        
        # Self-closing HTML5 tags
        self.self_closing = {
            'area', 'base', 'br', 'col', 'embed', 'hr', 'img', 'input', 
            'link', 'meta', 'param', 'source', 'track', 'wbr'
        }

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        
        if tag not in self.self_closing:
            self.tags_stack.append((tag, self.getpos()))
        
        if tag == 'a' and attrs_dict.get('class') == 'skip-link':
            self.has_skip_link = True
            if attrs_dict.get('href') != '#main-content':
                self.errors.append("Skip link href should point to '#main-content'")
        
        if tag == 'main' and attrs_dict.get('id') == 'main-content':
            self.has_main = True
        
        if tag == 'header':
            self.has_header = True
            
        if tag == 'footer':
            self.has_footer = True

        if tag == 'link' and attrs_dict.get('rel') == 'stylesheet' and attrs_dict.get('href') == 'styles.css':
            self.has_style = True
            
        if tag == 'label' and 'for' in attrs_dict:
            self.labels.add(attrs_dict['for'])
            
        if tag in ('input', 'textarea', 'select') and 'id' in attrs_dict:
            self.inputs.add(attrs_dict['id'])

    def handle_endtag(self, tag):
        if tag in self.self_closing:
            # Self-closing tags should not have end tags in HTML
            self.errors.append(f"Unexpected end tag </{tag}> for self-closing tag at line {self.getpos()[0]}")
            return
            
        if not self.tags_stack:
            self.errors.append(f"Unexpected end tag </{tag}> at line {self.getpos()[0]} (no open tags left)")
            return
        
        start_tag, pos = self.tags_stack.pop()
        if start_tag != tag:
            self.errors.append(f"Mismatched tags: <{start_tag}> opened at line {pos[0]} closed by </{tag}> at line {self.getpos()[0]}")

    def check_results(self):
        if self.tags_stack:
            for tag, pos in self.tags_stack:
                self.errors.append(f"Unclosed tag <{tag}> opened at line {pos[0]}")
        
        if not self.has_skip_link:
            self.errors.append("Missing keyboard accessibility skip link.")
        if not self.has_main:
            self.errors.append("Missing <main id=\"main-content\"> landmark.")
        if not self.has_header:
            self.errors.append("Missing <header> landmark.")
        if not self.has_footer:
            self.errors.append("Missing <footer> landmark.")
        if not self.has_style:
            self.errors.append("Missing reference to styles.css stylesheet.")
            
        for inp in self.inputs:
            if inp not in self.labels:
                self.errors.append(f"Input/textarea/select with id '{inp}' does not have a matching <label for='{inp}'>.")

        return self.errors

def validate_file(filepath):
    if not os.path.exists(filepath):
        print(f"❌ Error: File {filepath} not found.")
        return False
        
    with open(filepath, 'r', encoding='utf-8') as f:
        html_content = f.read()
        
    parser = HTMLValidator(os.path.basename(filepath))
    parser.feed(html_content)
    errors = parser.check_results()
    
    if errors:
        print(f"❌ Validation errors found in {os.path.basename(filepath)}:")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print(f"✅ HTML validation passed for {os.path.basename(filepath)}!")
        return True

def main():
    files = [
        'index.html',
        'team.html',
        'programs.html',
        'rates-insurance.html',
        'contact.html'
    ]
    
    all_passed = True
    for f in files:
        filepath = os.path.join('/Users/tarnett/Documents/BTNF_WEBSITE_OVERHAUL', f)
        if not validate_file(filepath):
            all_passed = False
            
    if not all_passed:
        sys.exit(1)
    else:
        print("\n🎉 All HTML pages are perfectly valid and structured!")
        sys.exit(0)

if __name__ == '__main__':
    main()
