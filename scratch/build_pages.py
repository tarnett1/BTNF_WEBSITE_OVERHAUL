import json
import os
import re

os.makedirs("scratch/data", exist_ok=True)

def load_json(filepath):
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)
    return []

staff_list = load_json("scratch/data/staff.json")
programs_list = load_json("scratch/data/programs.json")
other_data = load_json("scratch/data/other.json")

# Define template blocks
PROPOSAL_WIDGET_HTML = """
  <!-- Floating Collapsible Proposal Guide Widget -->
  <div class="proposal-widget collapsed" id="proposal-widget">
    <button class="proposal-widget-toggle" onclick="toggleProposalWidget()" aria-expanded="false" aria-label="Toggle proposal information guide">
      <span class="widget-toggle-icon">✨</span>
      <span class="widget-toggle-text">Proposal Guide &amp; Highlights</span>
      <span class="widget-toggle-arrow">▲</span>
    </button>
    <div class="proposal-widget-body">
      <h4>Interactive Website Proposal</h4>
      <p>This interactive concept draft demonstrates a modern, accessible structure for your new website.</p>
      <ul class="widget-highlights" style="margin: 10px 0; padding-left: 0; list-style: none; display: flex; flex-direction: column; gap: 8px;">
        <li style="position: relative; padding-left: 18px; font-size: 0.8rem; line-height: 1.4; color: var(--color-text-main);"><strong style="color: var(--color-primary-navy);">Multi-Page Layout:</strong> Proposed 5-page setup (Home, Programs, Team, Rates/Insurance, Contact) to present extensive copy clearly.</li>
        <li style="position: relative; padding-left: 18px; font-size: 0.8rem; line-height: 1.4; color: var(--color-text-main);"><strong style="color: var(--color-primary-navy);">Accessibility Standard:</strong> Custom high-contrast theme (including accessible deep gold and blue text), readable typography, and keyboard landmarks designed for reading/learning differences.</li>
        <li style="position: relative; padding-left: 18px; font-size: 0.8rem; line-height: 1.4; color: var(--color-text-main);"><strong style="color: var(--color-primary-navy);">Functional Portals:</strong> Links securely connect to your active intakes (Google Forms) and client portal (TherapyPortal).</li>
        <li style="position: relative; padding-left: 18px; font-size: 0.8rem; line-height: 1.4; color: var(--color-text-main);"><strong style="color: var(--color-primary-navy);">Concept Status:</strong> Copy and structure are drafts proposed to replace your original Google Site.</li>
      </ul>
      <p class="widget-note" style="font-size: 0.75rem; color: var(--color-text-muted); font-style: italic; border-top: 1px solid var(--color-border-subtle); padding-top: 6px; margin-top: 6px; margin-bottom: 0;">Marty &amp; Mike: Click this header to collapse/expand this guide.</p>
    </div>
  </div>
"""

NAV_HTML = PROPOSAL_WIDGET_HTML + """
  <!-- Keyboard Accessibility: Skip to Main Content Link -->
  <a href="#main-content" class="skip-link">Skip to main content</a>

  <!-- Main Navigation Header -->
  <header class="main-header">
    <div class="container header-container">
      <a href="index.html" class="logo-area" aria-label="Breakthroughs of North Florida Home">
        <img class="logo-img" src="logo.png" alt="Breakthroughs of North Florida Logo">
      </a>

      <!-- Desktop Navigation -->
      <nav class="main-nav" aria-label="Primary Navigation">
        <ul class="nav-list">
          <li><a href="index.html" class="nav-link">Home</a></li>
          <li><a href="programs.html" class="nav-link">Our Programs</a></li>
          <li><a href="team.html" class="nav-link">Meet the Team</a></li>
          <li><a href="rates-insurance.html" class="nav-link">Scholarships &amp; Insurance</a></li>
          <li><a href="contact.html" class="nav-link">Contact Us</a></li>
        </ul>
      </nav>

      <!-- Action Button -->
      <div class="header-cta">
        <a href="contact.html" class="btn btn-primary">Schedule Consultation</a>
      </div>

      <!-- Mobile Menu Toggle Button (Hamburger) -->
      <button class="menu-toggle" aria-expanded="false" aria-label="Toggle Navigation Menu">
        <span class="hamburger-bar"></span>
        <span class="hamburger-bar"></span>
        <span class="hamburger-bar"></span>
      </button>
    </div>

    <!-- Mobile Drawer Overlay Menu -->
    <nav class="mobile-nav" aria-label="Mobile Navigation">
      <ul class="mobile-nav-list">
        <li><a href="index.html" class="mobile-nav-link">Home</a></li>
        <li><a href="programs.html" class="mobile-nav-link">Our Programs</a></li>
        <li><a href="team.html" class="mobile-nav-link">Meet the Team</a></li>
        <li><a href="rates-insurance.html" class="mobile-nav-link">Scholarships &amp; Insurance</a></li>
        <li><a href="contact.html" class="mobile-nav-link">Contact Us</a></li>
        <li><a href="contact.html" class="btn btn-primary btn-block">Schedule Consultation</a></li>
      </ul>
    </nav>
  </header>
"""

FOOTER_HTML = """
  <!-- Global Footer -->
  <footer class="main-footer">
    <div class="container footer-container">
      <div class="footer-brand">
        <img class="logo-img" src="logo.png" alt="Breakthroughs of North Florida Logo">
        <p class="footer-desc">
          Professional, integrated therapeutic and educational care helping North Florida families thrive.
        </p>
      </div>

      <div class="footer-links-group">
        <div class="footer-links-col">
          <h5>Quick Links</h5>
          <ul>
            <li><a href="index.html">Home</a></li>
            <li><a href="programs.html">Our Programs</a></li>
            <li><a href="team.html">Meet the Team</a></li>
            <li><a href="rates-insurance.html">Rates &amp; Scholarships</a></li>
            <li><a href="contact.html">Contact Us</a></li>
          </ul>
        </div>
        <div class="footer-links-col">
          <h5>Legal &amp; Policy</h5>
          <ul>
            <li><a href="rates-insurance.html">Intake Forms</a></li>
            <li><a href="rates-insurance.html#privacy">Privacy Policy</a></li>
            <li><a href="contact.html#locations">Our Location</a></li>
          </ul>
        </div>
      </div>
    </div>
    
    <div class="footer-bottom">
      <div class="container footer-bottom-container">
        <div class="footer-legal-blocks">
          <p class="copyright-text">&copy; 2026 Breakthroughs of North Florida. All rights reserved.</p>
          <p class="license-info">Clinical mental health counseling services are provided by licensed clinicians in the State of Florida. Tutoring represents specialized academic intervention and does not constitute psychological therapy.</p>
          <p class="license-info"><strong>Affiliation Disclaimer:</strong> Breakthroughs of North Florida is not affiliated with, certified, endorsed, licensed, monitored or sponsored by Lindamood-Bell Learning Processes.</p>
        </div>
      </div>
    </div>
  </footer>

  <!-- Javascript for mobile menu toggling and proposal widget -->
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const menuToggle = document.querySelector('.menu-toggle');
      const mobileNav = document.querySelector('.mobile-nav');
      const mobileLinks = document.querySelectorAll('.mobile-nav-link');

      // Toggle mobile menu
      menuToggle.addEventListener('click', () => {
        const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
        menuToggle.setAttribute('aria-expanded', !expanded);
        menuToggle.classList.toggle('is-active');
        mobileNav.classList.toggle('is-active');
      });

      // Close mobile menu on link click
      mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
          menuToggle.setAttribute('aria-expanded', 'false');
          menuToggle.classList.remove('is-active');
          mobileNav.classList.remove('is-active');
        });
      });
    });

    // Toggle floating proposal widget
    function toggleProposalWidget() {
      const widget = document.getElementById('proposal-widget');
      if (widget) {
        const collapsed = widget.classList.toggle('collapsed');
        localStorage.setItem('proposal_widget_collapsed', collapsed ? 'true' : 'false');
        const toggleBtn = widget.querySelector('.proposal-widget-toggle');
        if (toggleBtn) {
          toggleBtn.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
        }
      }
    }

    // Restore proposal widget state
    document.addEventListener('DOMContentLoaded', () => {
      const isCollapsed = localStorage.getItem('proposal_widget_collapsed');
      const widget = document.getElementById('proposal-widget');
      if (widget && isCollapsed === 'false') {
        widget.classList.remove('collapsed');
        const toggleBtn = widget.querySelector('.proposal-widget-toggle');
        if (toggleBtn) {
          toggleBtn.setAttribute('aria-expanded', 'true');
        }
      }
    });
  </script>
"""

HEAD_TEMPL = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title} | Breakthroughs of North Florida</title>
  <meta name="description" content="{desc}">
  
  <!-- Google Fonts for Modern Typography -->
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  
  <link rel="stylesheet" href="styles.css">
  <style>
    /* Unique CSS overrides for secondary subpages */
    .subpage-hero {{
      background: var(--color-bg-alt);
      color: var(--color-text-main);
      padding: 5rem 0 4rem 0;
      text-align: center;
      border-bottom: 1px solid var(--color-border-subtle);
    }}
    .subpage-hero h1 {{
      color: var(--color-primary-navy);
      font-size: clamp(1.75rem, 5vw, 3rem);
      margin-bottom: 1rem;
      font-weight: 800;
      letter-spacing: -0.025em;
      word-wrap: break-word;
      overflow-wrap: break-word;
    }}
    .subpage-hero p {{
      color: var(--color-text-main);
      font-size: 1.25rem;
      max-width: 800px;
      margin: 0 auto;
      line-height: 1.6;
    }}
    
    /* Academic Theme overrides */
    .subpage-hero.hero-academic {{
      background: linear-gradient(135deg, #fefaf0 0%, #f5ecd5 100%);
      border-bottom-color: var(--color-academic-border);
    }}
    .subpage-hero.hero-academic h1 {{
      color: var(--color-academic-primary-dark);
    }}
    .subpage-hero.hero-academic p {{
      color: #3a2805;
    }}
    
    /* Counseling Theme overrides */
    .subpage-hero.hero-counseling {{
      background: linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%);
      border-bottom-color: var(--color-counseling-border);
    }}
    .subpage-hero.hero-counseling h1 {{
      color: var(--color-counseling-primary-dark);
    }}
    .subpage-hero.hero-counseling p {{
      color: #0f2b3c;
    }}
    
    /* Team Filtering styles */
    .filter-container {{
      display: flex;
      justify-content: center;
      gap: 1rem;
      margin: 3rem 0;
      flex-wrap: wrap;
    }}
    .filter-btn {{
      padding: 0.75rem 1.5rem;
      border: 1px solid var(--color-border-subtle);
      background-color: var(--color-bg-surface);
      border-radius: 50px;
      cursor: pointer;
      font-weight: 600;
      transition: all 0.2s ease;
    }}
    .filter-btn:hover {{
      background-color: var(--color-bg-alt);
    }}
    .filter-btn.active {{
      background-color: var(--color-primary-navy);
      color: var(--color-text-light);
      border-color: var(--color-primary-navy);
    }}
    
    /* Layout styling */
    .subpage-content {{
      padding: 4rem 0;
    }}
    
    .team-grid-extended {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(350px, 1fr));
      gap: 2.5rem;
    }}
    
    .team-bio-full {{
      margin-top: 1rem;
      font-size: 0.95rem;
      line-height: 1.6;
      color: var(--color-text-muted);
    }}
    
    .education-text {{
      font-style: italic;
      font-size: 0.9rem;
      color: var(--color-primary-navy);
      margin-top: 0.5rem;
      font-weight: 500;
    }}
    
    /* Section-based team layout */
    .section-title {{
      font-size: 2.25rem;
      color: var(--color-primary-navy);
      margin-top: 4.5rem;
      margin-bottom: 2rem;
      border-bottom: 2px solid var(--color-border-subtle);
      padding-bottom: 0.75rem;
      font-weight: 700;
      position: relative;
      letter-spacing: -0.02em;
    }}
    .section-title::after {{
      content: "";
      position: absolute;
      bottom: -2px;
      left: 0;
      width: 60px;
      height: 4px;
      background-color: var(--color-academic-primary);
      border-radius: 2px;
    }}
    .section-title.counseling-title::after {{
      background-color: var(--color-counseling-primary);
    }}
    .section-title.psychiatric-title::after {{
      background-color: #4338ca;
    }}
    .section-title.coaching-title::after {{
      background-color: #d97706;
    }}
    .leadership-card {{
      border-top: 4px solid var(--color-academic-primary) !important;
      background: linear-gradient(180deg, var(--color-bg-surface) 0%, var(--color-bg-alt) 100%) !important;
    }}
    .psychiatric-card {{
      border-top: 4px solid var(--color-counseling-primary) !important;
      background: linear-gradient(180deg, var(--color-bg-surface) 0%, var(--color-counseling-bg-light) 100%) !important;
    }}
    .team-grid-extended {{
      margin-bottom: 2rem;
    }}
    
    /* Programs layout */
    .programs-detailed {{
      display: flex;
      flex-direction: column;
      gap: 4rem;
    }}
    .program-card-detail {{
      background: var(--color-bg-surface);
      border: 1px solid var(--color-border-subtle);
      border-radius: 12px;
      padding: 3rem;
      box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
    }}
    .program-card-detail h3 {{
      font-size: 1.75rem;
      color: var(--color-primary-navy);
      margin-bottom: 1rem;
      border-left: 4px solid var(--color-academic-primary);
      padding-left: 1rem;
    }}
    .program-body-text {{
      line-height: 1.7;
      color: var(--color-text-muted);
      white-space: pre-wrap;
    }}
    
    /* Form & Insurance layout */
    .insurance-section-detail {{
      display: grid;
      grid-template-columns: 1fr 1.5fr;
      gap: 3rem;
      align-items: start;
    }}
    @media (max-width: 768px) {{
      .insurance-section-detail {{
        grid-template-columns: 1fr;
      }}
      .subpage-hero h1 {{
        font-size: 1.75rem;
      }}
    }}
    
    .insurance-list {{
      list-style: none;
      padding: 0;
    }}
    .insurance-list li {{
      padding: 0.75rem 1rem;
      background: var(--color-counseling-bg-light);
      border-left: 4px solid var(--color-counseling-primary);
      margin-bottom: 0.5rem;
      border-radius: 4px;
      font-weight: 600;
      color: var(--color-primary-navy);
    }}
    
    .paperwork-grid {{
      display: grid;
      grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
      gap: 1.5rem;
      margin-top: 2rem;
    }}
    
    .paperwork-card {{
      background: var(--color-bg-surface);
      border: 1px solid var(--color-border-subtle);
      border-radius: 8px;
      padding: 1.5rem;
      display: flex;
      flex-direction: column;
      justify-content: space-between;
      height: 100%;
    }}
    .paperwork-card h4 {{
      margin-bottom: 0.5rem;
      color: var(--color-text-main);
    }}
    .paperwork-card p {{
      font-size: 0.85rem;
      color: var(--color-text-muted);
      margin-bottom: 1.5rem;
    }}
    
    /* Contact page overrides */
    .contact-grid-detail {{
      display: grid;
      grid-template-columns: 1fr 1fr;
      gap: 4rem;
    }}
    @media (max-width: 768px) {{
      .contact-grid-detail {{
        grid-template-columns: 1fr;
      }}
    }}
    
    .map-frame {{
      width: 100%;
      height: 350px;
      border: 0;
      border-radius: 8px;
      margin-top: 1.5rem;
    }}
    
    .card-portal-box {{
      background: var(--color-bg-alt);
      border-radius: 12px;
      padding: 2.5rem;
      margin-bottom: 2rem;
      border: 1px solid var(--color-border-subtle);
    }}
  </style>
</head>
<body>
"""

# Build team.html
def build_team():
    team_html = HEAD_TEMPL.format(
        title="Meet Our Team | Therapists & Educational Specialists",
        desc="Meet the clinical psychologists, licensed marriage and family therapists, and tutoring specialists at Breakthroughs of North Florida."
    )
    team_html += NAV_HTML
    
    # Separate lists
    leadership_keys = ["marty-edwards", "lizz-arnett", "devin-mcclure"]
    leadership_team = [m for m in staff_list if m["key"] in leadership_keys]
    
    psychiatric_team = [m for m in staff_list if m["key"] == "casey-goss"]
    coaching_team = [m for m in staff_list if m["key"] == "madison-moore"]
    
    # Filter counseling and education keeping leadership visible in their respective functional grids as well
    counseling_team = [m for m in staff_list if m["category"] == "counseling" and m["key"] != "marty-edwards"]
    education_team = [m for m in staff_list if m["category"] == "education"]
    
    # Helper to generate a single staff card
    def make_card(member, extra_classes=""):
        cat = member["category"]
        badge_class = "badge-counseling"
        if cat == "education":
            badge_class = "badge-academic"
        elif cat == "psychiatric":
            badge_class = ""
            
        badge_style = ""
        if cat == "psychiatric":
            badge_style = 'style="background-color: #e0e7ff; color: #4338ca; border: 1px solid #c7d2fe;"'
            
        role_label = member["role"]
        edu_label = member["education"]
        bio = member["bio"]
        
        # Format team badge text
        badge_text = cat.title() + " Team"
        if cat == "coaching":
            badge_text = "Life Coaching"
            badge_style = 'style="background-color: #fef3c7; color: #d97706; border: 1px solid #fde68a;"'
        elif cat == "psychiatric":
            badge_text = "Psychiatric Services"
            
        return f"""
          <!-- Staff Card: {member["name"]} -->
          <div class="team-card {extra_classes}" data-category="{cat}">
            <div class="team-card-header">
              <img class="team-avatar" src="{member["image"]}" alt="{member["name"]}">
              <div class="team-meta">
                <h4>{member["name"]}</h4>
                <span class="team-role">{role_label}</span>
                <span class="team-badge {badge_class}" {badge_style}>{badge_text}</span>
              </div>
            </div>
            {f'<p class="education-text">{edu_label}</p>' if edu_label else ''}
            <p class="team-bio-full">{bio}</p>
          </div>
        """

    team_html += """
  <main id="main-content">
    <section class="subpage-hero">
      <div class="container">
        <h1>Meet Our Dedicated Specialists</h1>
        <p>Our multidisciplinary team of licensed therapists, clinical supervisors, and certified educational specialists coordinates support for your family's growth and success.</p>
      </div>
    </section>

    <section class="subpage-content">
      <div class="container">
        <!-- Interactive filter buttons (Jump Links) -->
        <div class="filter-container" style="position: sticky; top: 80px; z-index: 99; background: var(--color-bg-surface); padding: 1rem 0; border-bottom: 1px solid var(--color-border-subtle);">
          <button class="filter-btn active" data-target="leadership">Leadership &amp; Operations</button>
          <button class="filter-btn" data-target="counseling">Counseling &amp; Therapy</button>
          <button class="filter-btn" data-target="psychiatric">Psychiatric Services</button>
          <button class="filter-btn" data-target="education">Educational &amp; Tutoring</button>
          <button class="filter-btn" data-target="coaching">Life Coaching</button>
        </div>

        <!-- Section 1: Leadership & Operations -->
        <div id="leadership" class="team-section-block">
          <h2 class="section-title">Clinical Leadership &amp; Operations</h2>
          <div class="team-grid-extended">
    """
    
    for member in leadership_team:
        team_html += make_card(member, "leadership-card")
        
    team_html += """
          </div>
        </div>

        <!-- Section 2: Clinical Counseling Team -->
        <div id="counseling" class="team-section-block">
          <h2 class="section-title counseling-title">Clinical Counseling &amp; Therapy</h2>
          <div class="team-grid-extended">
    """
    
    for member in counseling_team:
        team_html += make_card(member)
        
    team_html += """
          </div>
        </div>

        <!-- Section 3: Psychiatric Services -->
        <div id="psychiatric" class="team-section-block">
          <h2 class="section-title psychiatric-title">Psychiatric Services</h2>
          <div class="team-grid-extended">
    """
    
    for member in psychiatric_team:
        team_html += make_card(member, "psychiatric-card")
        
    team_html += """
          </div>
        </div>

        <!-- Section 4: Specialized Educational & Tutoring Team -->
        <div id="education" class="team-section-block">
          <h2 class="section-title">Specialized Educational &amp; Tutoring</h2>
          <div class="team-grid-extended">
    """
    
    for member in education_team:
        team_html += make_card(member)
        
    team_html += """
          </div>
        </div>

        <!-- Section 5: Life Coaching -->
        <div id="coaching" class="team-section-block">
          <h2 class="section-title coaching-title">Life Coaching</h2>
          <div class="team-grid-extended">
    """
    
    for member in coaching_team:
        team_html += make_card(member)
        
    team_html += """
          </div>
        </div>

      </div>
    </section>
  </main>
  
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const filterBtns = document.querySelectorAll('.filter-btn');
      
      filterBtns.forEach(btn => {
        btn.addEventListener('click', (e) => {
          e.preventDefault();
          const targetId = btn.getAttribute('data-target');
          const targetSection = document.getElementById(targetId);
          if (targetSection) {
            const headerHeight = document.querySelector('.main-header').offsetHeight;
            const filterContainerHeight = document.querySelector('.filter-container').offsetHeight;
            const targetPosition = targetSection.getBoundingClientRect().top + window.pageYOffset - headerHeight - filterContainerHeight - 20;
            
            window.scrollTo({
              top: targetPosition,
              behavior: 'smooth'
            });
            
            // Update active button state
            filterBtns.forEach(b => b.classList.remove('active'));
            btn.classList.add('active');
          }
        });
      });
      
      // Update active button on scroll
      window.addEventListener('scroll', () => {
        const sections = document.querySelectorAll('.team-section-block');
        const headerHeight = document.querySelector('.main-header').offsetHeight;
        const filterContainerHeight = document.querySelector('.filter-container').offsetHeight;
        let currentActive = 'leadership';
        
        sections.forEach(sec => {
          const top = sec.offsetTop - headerHeight - filterContainerHeight - 60;
          if (window.pageYOffset >= top) {
            currentActive = sec.getAttribute('id');
          }
        });
        
        filterBtns.forEach(btn => {
          if (btn.getAttribute('data-target') === currentActive) {
            btn.classList.add('active');
          } else {
            btn.classList.remove('active');
          }
        });
      });
    });
  </script>
    """
    
    team_html += FOOTER_HTML
    team_html += "</body>\n</html>"
    
    with open("team.html", "w", encoding="utf-8") as f:
        f.write(team_html)
    print("Generated team.html")

# Build programs.html
def build_programs():
    prog_html = HEAD_TEMPL.format(
        title="Our Educational Programs | Barton Spelling & Lindamood-Bell",
        desc="Learn about our research-backed academic methodologies: Barton Reading and Spelling, Lindamood-Bell instruction, SAT/ACT Prep, and Love and Logic."
    )
    prog_html += NAV_HTML
    
    prog_html += """
  <main id="main-content">
    <section class="subpage-hero hero-academic">
      <div class="container">
        <h1>Specialized Educational Programs</h1>
        <p>Research-based academic interventions customized for neurodivergent learners, homeschoolers, and students with unique learning styles.</p>
      </div>
    </section>

    <section class="subpage-content">
      <div class="container">
        <div class="programs-detailed">
    """
    
    for prog in programs_list:
        title = prog["title"]
        text = prog["text"]
        
        prog_html += f"""
          <article class="program-card-detail" id="{prog["key"]}">
            <h3>{title}</h3>
            <div class="program-body-text">{text}</div>
          </article>
        """
        
    prog_html += """
        </div>
      </div>
    </section>
  </main>
    """
    
    prog_html += FOOTER_HTML
    prog_html += "</body>\n</html>"
    
    with open("programs.html", "w", encoding="utf-8") as f:
        f.write(prog_html)
    print("Generated programs.html")

# Build rates-insurance.html
def build_rates_insurance():
    rates_html = HEAD_TEMPL.format(
        title="Rates, Scholarships, & Intake Forms | Yulee Services",
        desc="View accepted health insurance networks, Florida PEP/FES scholarship details, and download intake paperwork for new clients."
    )
    rates_html += NAV_HTML
    
    privacy_copy = other_data.get("privacy-policy", {}).get("text", "Privacy policy details.")
    
    rates_html += f"""
  <main id="main-content">
    <section class="subpage-hero hero-counseling">
      <div class="container">
        <h1>Scholarships, Insurance, &amp; Paperwork</h1>
        <p>Accepted health insurance networks, Florida scholarships (Step Up for Students), and new client intake paperwork download links.</p>
      </div>
    </section>

    <section class="subpage-content">
      <div class="container">
        
        <div class="insurance-section-detail">
          <div>
            <h3>Accepted Health Insurances</h3>
            <p style="margin-bottom: 1.5rem; color: var(--color-text-muted);">Health insurance coverage applies to clinical mental health counseling and therapeutic services only. We are in-network with the following major providers:</p>
            <div class="badge-row" style="display: flex; flex-wrap: wrap; gap: 1rem; margin-top: 1.5rem;">
              <div class="insurance-logo-card" aria-label="Florida Blue Cross Blue Shield accepted">
                <img src="images/bcbs_logo.svg" alt="Florida Blue Logo">
              </div>
              <div class="insurance-logo-card" aria-label="UnitedHealthcare accepted">
                <img src="images/uhc_logo.svg" alt="UnitedHealthcare Logo">
              </div>
              <div class="insurance-logo-card" aria-label="Tricare Insurance accepted">
                <img src="images/tricare_logo.svg" alt="Tricare Logo">
              </div>
              <div class="insurance-logo-card" aria-label="Aetna Insurance accepted">
                <img src="images/aetna_logo.svg" alt="Aetna Logo">
              </div>
              <div class="insurance-logo-card" aria-label="Cigna Insurance accepted">
                <img src="images/cigna_logo.svg" alt="Cigna Logo">
              </div>
            </div>
          </div>
          <div>
            <h3>Florida Scholarship Programs</h3>
            <p style="margin-bottom: 1rem; color: var(--color-text-muted);">Breakthroughs of North Florida is an approved educational provider for the <strong>Step Up for Students</strong> scholarship network. Families can utilize scholarship awards to cover educational tutoring, Barton, and Lindamood-Bell® specialized programs:</p>
            <div class="card-portal-box" style="margin-bottom: 1rem;">
              <h4 style="color: var(--color-primary-navy);">Family Empowerment Scholarship - Unique Abilities (FES-UA)</h4>
              <p style="font-size: 0.95rem; color: var(--color-text-muted); margin-top: 0.5rem;">For students with identified unique abilities or diagnosis. FES-UA funding can be utilized to directly cover the cost of customized educational tutoring and sensory-cognitive programs.</p>
            </div>
            <div class="card-portal-box">
              <h4 style="color: var(--color-primary-navy);">Personalized Education Program (PEP) / Florida Choice</h4>
              <p style="font-size: 0.95rem; color: var(--color-text-muted); margin-top: 0.5rem;">For homeschool or personalized educational paths. Award funds can be applied toward Barton spelling, Lindamood-Bell methods, and curriculum support sessions.</p>
            </div>
          </div>
        </div>

        <hr style="margin: 4rem 0; border: 0; border-top: 1px solid var(--color-border-subtle);">

        <div id="forms">
          <h3>Client Forms &amp; Paperwork</h3>
          <p style="color: var(--color-text-muted); margin-bottom: 1.5rem;">Please review, print, and complete the appropriate intake packet prior to your first session. This ensures a smooth onboarding process for your family.</p>
          
          <div class="paperwork-grid">
            <div class="paperwork-card">
              <div>
                <h4>Counseling Intake Packet</h4>
                <p>For new clinical mental health clients. Includes clinical disclosures, consent to treat, and history intake.</p>
              </div>
              <a href="https://forms.gle/X3RCMwhWqUVp6wNT8" target="_blank" rel="noopener noreferrer" class="btn btn-secondary btn-block">Complete Online Intake</a>
            </div>
            
            <div class="paperwork-card">
              <div>
                <h4>Academic &amp; Tutoring Intake</h4>
                <p>For educational services, Barton tutoring, and Lindamood-Bell programs. Includes academic profile forms.</p>
              </div>
              <a href="https://forms.gle/X3RCMwhWqUVp6wNT8" target="_blank" rel="noopener noreferrer" class="btn btn-secondary btn-block">Complete Academic Intake</a>
            </div>

            <div class="paperwork-card">
              <div>
                <h4>TherapyNotes® Disclosures</h4>
                <p>Mandatory privacy disclosures, HIPAA agreements, and billing consent forms for insurance submission.</p>
              </div>
              <a href="https://www.therapyportal.com/p/breakthroughs32097/" target="_blank" class="btn btn-secondary btn-block">Access Client Portal</a>
            </div>
          </div>
        </div>

        <hr style="margin: 4rem 0; border: 0; border-top: 1px solid var(--color-border-subtle);">

        <div id="privacy">
          <h3>Privacy Policy &amp; Disclosures</h3>
          <div style="font-size: 0.95rem; line-height: 1.6; color: var(--color-text-muted); white-space: pre-wrap;">{privacy_copy}</div>
        </div>

      </div>
    </section>
  </main>
    """
    
    rates_html += FOOTER_HTML
    rates_html += "</body>\n</html>"
    
    with open("rates-insurance.html", "w", encoding="utf-8") as f:
        f.write(rates_html)
    print("Generated rates-insurance.html")

# Build contact.html
def build_contact():
    contact_html = HEAD_TEMPL.format(
        title="Contact Us & Intake Portals | Breakthroughs of North Florida",
        desc="Contact our Yulee office, locate us in Professional Way, or access TherapyPortal and monday.com onboarding portals."
    )
    contact_html += NAV_HTML
    
    contact_html += """
  <main id="main-content">
    <section class="subpage-hero">
      <div class="container">
        <h1>Connect With Our Team</h1>
        <p>Get in touch for consultations, intake packets, location details, and active client portal access.</p>
      </div>
    </section>

    <section class="subpage-content">
      <div class="container">
        <div class="contact-grid-detail">
          <div>
            <h3>Office Contact &amp; Details</h3>
            <p style="color: var(--color-text-muted); margin-bottom: 2rem;">If you have questions about scheduling, billing, insurance, or specific tutoring methodologies, reach out directly or schedule an initial consultation below.</p>
            
            <div class="card-portal-box" style="margin-bottom: 2rem;">
              <h4 style="margin-bottom: 0.5rem; color: var(--color-primary-navy);">Call Our Office</h4>
              <p style="font-size: 1.25rem; font-weight: 700; color: var(--color-text-main);"><a href="tel:9048491190" style="color: inherit; text-decoration: none;">904-849-1190</a></p>
              <p style="font-size: 0.85rem; color: var(--color-text-muted); margin-top: 0.25rem;">Monday - Friday: 8:00 AM - 6:00 PM</p>
            </div>

            <div class="card-portal-box" style="margin-bottom: 2rem;">
              <h4 style="margin-bottom: 0.5rem; color: var(--color-primary-navy);">Email Address</h4>
              <p style="font-size: 1.15rem; font-weight: 600; color: var(--color-text-main);"><a href="mailto:office@breakthroughsnf.com" style="color: inherit; text-decoration: underline;">office@breakthroughsnf.com</a></p>
              <p style="font-size: 0.85rem; color: var(--color-text-muted); margin-top: 0.25rem;">For general inquiries, scholarship verification, and records.</p>
            </div>

            <div id="locations">
              <h3>Office Location</h3>
              <p style="color: var(--color-text-muted);">We are conveniently located in Yulee, serving Fernandina Beach, Amelia Island, and Nassau County:</p>
              <p style="font-weight: 600; color: var(--color-text-main); margin: 0.5rem 0;">87003 Professional Way<br>Yulee, Florida 32097</p>
              <iframe class="map-frame" src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1m2!1s0x88e44c20579e0bf5%3A0xe9ee95e5ef0de367!2s87003%20Professional%20Way%2C%20Yulee%2C%20FL%2032097!5e0!3m2!1sen!2sus!4v1717900000000!5m2!1sen!2sus" allowfullscreen="" loading="lazy"></iframe>
            </div>
          </div>

          <div>
            <h3>Secure Client Portals</h3>
            <p style="color: var(--color-text-muted); margin-bottom: 2rem;">Access billing statements, schedule appointments, and submit documentation securely through our clinical and educational onboarding portals:</p>
            
            <div class="card-portal-box" style="border-left: 5px solid var(--color-counseling-primary); background: var(--color-counseling-bg-light);">
              <h4 style="color: var(--color-counseling-primary);">Counseling Client Portal</h4>
              <p style="font-size: 0.95rem; color: var(--color-text-muted); margin: 0.5rem 0 1.5rem 0;">Existing clinical mental health counseling clients can access invoices, session scheduling, and HIPAA documentation via TherapyPortal.</p>
              <a href="https://www.therapyportal.com/p/breakthroughs32097/" target="_blank" rel="noopener noreferrer" class="btn btn-primary" style="background-color: var(--color-counseling-primary); border-color: var(--color-counseling-primary);">Access TherapyPortal</a>
            </div>

            <div class="card-portal-box" style="border-left: 5px solid var(--color-academic-primary); background: var(--color-academic-bg-light);">
              <h4 style="color: var(--color-academic-primary);">Academic &amp; Tutoring Board</h4>
              <p style="font-size: 0.95rem; color: var(--color-text-muted); margin: 0.5rem 0 1.5rem 0;">New educational, tutoring, and Lindamood-Bell® families can fill out the intake registration and track their onboarding workflows on our monday.com dashboard.</p>
              <a href="https://forms.gle/X3RCMwhWqUVp6wNT8" target="_blank" class="btn btn-primary" style="background-color: var(--color-academic-primary); border-color: var(--color-academic-primary);">Academic Intake Onboarding</a>
            </div>
            
            <div class="card-portal-box">
              <h4>Send Us a Message</h4>
              <p style="font-size: 0.95rem; color: var(--color-text-muted); margin-bottom: 1.5rem;">Would you like us to contact you? Let us know what services you are interested in.</p>
              <a href="index.html#contact" class="btn btn-secondary btn-block">Go to Consultation Form</a>
            </div>
          </div>
        </div>
      </div>
    </section>
  </main>
    """
    
    contact_html += FOOTER_HTML
    contact_html += "</body>\n</html>"
    
    with open("contact.html", "w", encoding="utf-8") as f:
        f.write(contact_html)
    print("Generated contact.html")

# Update index.html navigation links
def update_index_links():
    filepath = "index.html"
    if not os.path.exists(filepath):
        print(f"Error: {filepath} not found.")
        return
        
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
        
    # Clean existing banner/widget to avoid duplicates
    content = re.sub(
        r'<!-- Concept Proposal Banner -->.*?<!-- Keyboard Accessibility: Skip to Main Content Link -->',
        '<!-- Keyboard Accessibility: Skip to Main Content Link -->',
        content,
        flags=re.DOTALL
    )
    content = re.sub(
        r'<!-- Floating Collapsible Proposal Guide Widget -->.*?<!-- Keyboard Accessibility: Skip to Main Content Link -->',
        '<!-- Keyboard Accessibility: Skip to Main Content Link -->',
        content,
        flags=re.DOTALL
    )
    # Insert proposal widget
    content = content.replace("<body>", "<body>\n" + PROPOSAL_WIDGET_HTML)
        
    # Replace navbar links
    # Desktop links
    content = content.replace(
        '<a href="#services" class="nav-link">Our Services</a>',
        '<a href="programs.html" class="nav-link">Our Programs</a>'
    )
    content = content.replace(
        '<a href="#portals" class="nav-link">Client Portals</a>',
        '<a href="contact.html" class="nav-link">Client Portals</a>'
    )
    content = content.replace(
        '<a href="#badges" class="nav-link">Scholarships &amp; Insurance</a>',
        '<a href="rates-insurance.html" class="nav-link">Scholarships &amp; Insurance</a>'
    )
    content = content.replace(
        '<a href="#team" class="nav-link">Meet the Team</a>',
        '<a href="team.html" class="nav-link">Meet the Team</a>'
    )
    content = content.replace(
        '<a href="#contact" class="nav-link">Contact Us</a>',
        '<a href="contact.html" class="nav-link">Contact Us</a>'
    )
    
    # Mobile links
    content = content.replace(
        '<a href="#services" class="mobile-nav-link">Our Services</a>',
        '<a href="programs.html" class="mobile-nav-link">Our Programs</a>'
    )
    content = content.replace(
        '<a href="#portals" class="mobile-nav-link">Client Portals</a>',
        '<a href="contact.html" class="mobile-nav-link">Client Portals</a>'
    )
    content = content.replace(
        '<a href="#badges" class="mobile-nav-link">Scholarships &amp; Insurance</a>',
        '<a href="rates-insurance.html" class="mobile-nav-link">Scholarships &amp; Insurance</a>'
    )
    content = content.replace(
        '<a href="#team" class="mobile-nav-link">Meet the Team</a>',
        '<a href="team.html" class="mobile-nav-link">Meet the Team</a>'
    )
    content = content.replace(
        '<a href="#contact" class="mobile-nav-link">Contact Us</a>',
        '<a href="contact.html" class="mobile-nav-link">Contact Us</a>'
    )
    
    # Footer links
    content = content.replace(
        '<li><a href="#services">Our Services</a></li>',
        '<li><a href="programs.html">Our Programs</a></li>'
    )
    content = content.replace(
        '<li><a href="#portals">Client Portals</a></li>',
        '<li><a href="contact.html">Client Portals</a></li>'
    )
    content = content.replace(
        '<li><a href="#badges">Scholarships &amp; Insurance</a></li>',
        '<li><a href="rates-insurance.html">Scholarships &amp; Insurance</a></li>'
    )
    content = content.replace(
        '<li><a href="#about">About &amp; Team</a></li>',
        '<li><a href="team.html">Meet the Team</a></li>'
    )
    content = content.replace(
        '<li><a href="#contact">Contact &amp; Intake</a></li>',
        '<li><a href="contact.html">Contact Us</a></li>'
    )
    
    # CTA button hrefs
    content = content.replace('href="#contact" class="btn btn-primary"', 'href="contact.html" class="btn btn-primary"')
    content = content.replace('href="#contact" class="btn btn-primary btn-block"', 'href="contact.html" class="btn btn-primary btn-block"')
    content = content.replace('href="#contact" class="btn btn-secondary btn-block"', 'href="contact.html" class="btn btn-secondary btn-block"')
    
    # Hero/Path card buttons
    content = content.replace('href="#services-counseling" class="btn btn-secondary', 'href="programs.html#lindamood-bell" class="btn btn-secondary')
    content = content.replace('href="#services-academic" class="btn btn-secondary', 'href="programs.html#tutoring" class="btn btn-secondary')
    
    # "Find Your Match" button in team card
    content = content.replace('href="#contact" class="btn btn-secondary btn-block"', 'href="contact.html" class="btn btn-secondary btn-block"')
    content = content.replace('href="#contact" class="btn btn-primary btn-block"', 'href="contact.html" class="btn btn-primary btn-block"')
    
    # Team section block in index.html footer CTA link
    content = content.replace('href="#contact" class="btn btn-secondary btn-block"', 'href="contact.html" class="btn btn-secondary btn-block"')
    
    # Also clean and insert script in index.html script block if it isn't already there
    index_old_script = """  <!-- Javascript for mobile menu toggling and smooth scrolling -->
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const menuToggle = document.querySelector('.menu-toggle');
      const mobileNav = document.querySelector('.mobile-nav');
      const mobileLinks = document.querySelectorAll('.mobile-nav-link');

      // Toggle mobile menu
      menuToggle.addEventListener('click', () => {
        const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
        menuToggle.setAttribute('aria-expanded', !expanded);
        menuToggle.classList.toggle('is-active');
        mobileNav.classList.toggle('is-active');
      });

      // Close mobile menu on link click
      mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
          menuToggle.setAttribute('aria-expanded', 'false');
          menuToggle.classList.remove('is-active');
          mobileNav.classList.remove('is-active');
        });
      });
    });
  </script>"""

    index_new_script = """  <!-- Javascript for mobile menu toggling and smooth scrolling -->
  <script>
    document.addEventListener('DOMContentLoaded', () => {
      const menuToggle = document.querySelector('.menu-toggle');
      const mobileNav = document.querySelector('.mobile-nav');
      const mobileLinks = document.querySelectorAll('.mobile-nav-link');

      // Toggle mobile menu
      menuToggle.addEventListener('click', () => {
        const expanded = menuToggle.getAttribute('aria-expanded') === 'true';
        menuToggle.setAttribute('aria-expanded', !expanded);
        menuToggle.classList.toggle('is-active');
        mobileNav.classList.toggle('is-active');
      });

      // Close mobile menu on link click
      mobileLinks.forEach(link => {
        link.addEventListener('click', () => {
          menuToggle.setAttribute('aria-expanded', 'false');
          menuToggle.classList.remove('is-active');
          mobileNav.classList.remove('is-active');
        });
      });
    });

    // Toggle floating proposal widget
    function toggleProposalWidget() {
      const widget = document.getElementById('proposal-widget');
      if (widget) {
        const collapsed = widget.classList.toggle('collapsed');
        localStorage.setItem('proposal_widget_collapsed', collapsed ? 'true' : 'false');
        const toggleBtn = widget.querySelector('.proposal-widget-toggle');
        if (toggleBtn) {
          toggleBtn.setAttribute('aria-expanded', collapsed ? 'false' : 'true');
        }
      }
    }

    // Restore proposal widget state
    document.addEventListener('DOMContentLoaded', () => {
      const isCollapsed = localStorage.getItem('proposal_widget_collapsed');
      const widget = document.getElementById('proposal-widget');
      if (widget && isCollapsed === 'false') {
        widget.classList.remove('collapsed');
        const toggleBtn = widget.querySelector('.proposal-widget-toggle');
        if (toggleBtn) {
          toggleBtn.setAttribute('aria-expanded', 'true');
        }
      }
    });
  </script>"""
    
    content = content.replace(index_old_script, index_new_script)

    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
    print("Updated index.html links.")

if __name__ == "__main__":
    build_team()
    build_programs()
    build_rates_insurance()
    build_contact()
    update_index_links()
