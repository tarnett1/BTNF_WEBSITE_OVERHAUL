# Issue & Enhancement Tracker — Breakthroughs of North Florida Website Overhaul

This tracker monitors the status of design concept enhancements, active bug fixes, and copywriting edits proposed for the website migration skeleton.

---

## 📋 Concept & Skeleton Status
- **Overall Status**: **Draft Skeleton / Interactive Proposal**
- **Deployment**: Live at [tarnett1.github.io/BTNF_WEBSITE_OVERHAUL](https://tarnett1.github.io/BTNF_WEBSITE_OVERHAUL/)
- **Goals**: Demonstrate multi-page structure, accessible typography/colors, secure intake portals, and interactive team catalogs.

---

## 🐛 Bug Fixes & UX Optimization

| Category | Issue Description | Priority | Status | Resolution |
| :--- | :--- | :---: | :---: | :--- |
| **Navigation** | Top nav menu items disappearing/changing dynamically on subpages | High | `[x]` Resolved | Standardized `NAV_HTML` across all pages (including `index.html`). Standardized all footer quick links. Aligned mobile menu switch breakpoints to `992px` and added layout-responsive font/gap scaling for viewports under `1200px` to prevent overflow-wrapping from clipping links. |
| **Integrations** | Google Maps embed failing with "Invalid pb parameter" error | High | `[x]` Resolved | Removed complex `pb` API hash parameters and swapped with a clean, cached query location parameter (`q=87003+Professional+Way...`). |
| **Mobile UX** | Mobile nav menu drawer links going off-screen and unscrollable on small screens | Medium | `[x]` Resolved | Raised `.mobile-nav` z-index to `150` and added `max-height: calc(100vh - 100%)` with `overflow-y: auto`. |
| **Accessibility** | Banner titles at the top of pages are dark on dark and hard to read | High | `[x]` Resolved | Redesigned heroes to use soft light gradient themes with high-contrast, accessible dark titles. |

---

## 🚀 Enhancements & Restructuring

| Section / Page | Requested Enhancement | Priority | Status | Details |
| :--- | :--- | :---: | :---: | :--- |
| **Homepage** | Feature only Marty, Mike, and Devin in team spotlight (no Lizz or Casey) | High | `[x]` Resolved | Replaced Lizz and Casey featured cards with Devin and Mike on the homepage spotlight. |
| **Team Page** | Restructure Team section order and add Mike Edwards to leadership grid | High | `[x]` Resolved | Restructured leadership keys to exactly Devin, Marty, and Mike. Downloaded Mike's profile photo and bio. |
| **Team Page** | Move Lizz Arnett under Educational Services and add Alex reporting line | High | `[x]` Resolved | Re-categorized Lizz in education and added "Reports to: Alex Beveridge" under her title. |
| **Team Cards** | Shorten staff cards and implement collapsible bios to manage infinite scroll | High | `[x]` Resolved | Programmed page compiler to truncate bios at the first natural sentence and embed a styled "Read More" toggle. |
| **Proposal Guide** | Rework floating widget copy to pitch recommendations and remove personal names | Medium | `[x]` Resolved | Reworked copy to serve as an "Enhancement Guide & Concept Highlights", removing names and emphasizing the prototype status. |
| **Branding** | Replace clinical partnership details with direct clinic integration details | Medium | `[x]` Resolved | Cleaned "Sound Mind Solutions" credentials and branding from all clinical cards and staff bio databases. |
| **Rates Page** | Replace text lists of accepted insurances with visual brand logos | Medium | `[x]` Resolved | Generated vector SVGs (Aetna, Blue Cross, Cigna, UHC, Tricare) and placed them in animated hover cards. |
| **Accessibility** | Improve color contrast for users with reading/learning differences | High | `[x]` Resolved | Integrated accessible HSL dark colors (`#735414` gold, `#025a8b` blue) to achieve WCAG AA compliance. |

---

*This tracker will continue to be updated as design iterations and final assets are completed.*
