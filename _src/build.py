#!/usr/bin/env python3
"""Rapture Ready Home Care — static site generator.

Edit content here, then run:  python3 _src/build.py
Every page is written as <slug>/index.html so the old site's URLs keep working.
Built by Truly Digital Solutions, LLC (TruTech) · Build TT-RR-2026-04
"""
import html, json, os, re
from datetime import date

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BUILD_ID = 'TT-RR-2026-04'
DOMAIN = 'https://www.rapturereadyhomecare.com'

B = {
    'name': 'Rapture Ready Home Care',
    'phone': '1 (252) 503-2978', 'tel': '+12525032978',
    'fax': '1 (910) 333-0128',
    'email': 'Contact@raptureready.care',
    'street': '625 College St.', 'city': 'Jacksonville, NC 28540',
    'map': 'https://maps.google.com/maps?q=625+College+St.%2C+Jacksonville%2C+NC+28540',
    'npi': '1720889108',
    'hours': 'Monday – Friday, 9:00 am – 5:00 pm',
    'hours_short': 'Mon – Fri, 9 am – 5 pm',
    'sister': 'https://www.faithfulridesllc.com',
}

esc = html.escape


# ---------------------------------------------------------------------------
# Icons (1.6px line icons, inherit currentColor)
# ---------------------------------------------------------------------------
def icon(name, cls='ic'):
    p = {
        'phone': '<path d="M5 4h3.5l1.6 4.2-2.2 1.4a11 11 0 0 0 6.5 6.5l1.4-2.2L20 15.5V19a1.5 1.5 0 0 1-1.6 1.5A16.5 16.5 0 0 1 3.5 5.6 1.5 1.5 0 0 1 5 4Z"/>',
        'mail': '<rect x="3" y="5" width="18" height="14" rx="2"/><path d="m3.5 6.5 8.5 6.5 8.5-6.5"/>',
        'pin': '<path d="M12 21s-7-6.2-7-11.5a7 7 0 0 1 14 0C19 14.8 12 21 12 21Z"/><circle cx="12" cy="9.5" r="2.5"/>',
        'clock': '<circle cx="12" cy="12" r="8.5"/><path d="M12 7.5V12l3 2"/>',
        'shield': '<path d="M12 3 5 6v5.5c0 4.3 3 7.8 7 9.5 4-1.7 7-5.2 7-9.5V6l-7-3Z"/><path d="m9 12 2 2 4-4"/>',
        'card': '<rect x="3" y="5.5" width="18" height="13" rx="2"/><path d="M3 10h18M7 15h4"/>',
        'calendar': '<rect x="3.5" y="5" width="17" height="15" rx="2"/><path d="M3.5 10h17M8 3v4M16 3v4"/>',
        'heart': '<path d="M12 20s-7.5-4.6-7.5-10.1A4.3 4.3 0 0 1 12 7.3a4.3 4.3 0 0 1 7.5 2.6C19.5 15.4 12 20 12 20Z"/>',
        'sun': '<circle cx="12" cy="12" r="4"/><path d="M12 2.5v2M12 19.5v2M4.6 4.6l1.4 1.4M18 18l1.4 1.4M2.5 12h2M19.5 12h2M4.6 19.4 6 18M18 6l1.4-1.4"/>',
        'moon': '<path d="M19.5 14.5A8 8 0 0 1 9.5 4.5a8 8 0 1 0 10 10Z"/>',
        'home': '<path d="M4 11 12 4l8 7"/><path d="M6 9.5V20h12V9.5"/><path d="M10 20v-5h4v5"/>',
        'spark': '<path d="M12 3v4M12 17v4M3 12h4M17 12h4M6 6l2.5 2.5M15.5 15.5 18 18M6 18l2.5-2.5M15.5 8.5 18 6"/>',
        'check': '<path d="m5 12.5 4.5 4.5L19 7.5"/>',
        'arrow': '<path d="M5 12h14M13 6l6 6-6 6"/>',
        'back': '<path d="M19 12H5M11 6l-6 6 6 6"/>',
        'van': '<path d="M3 16V8a1 1 0 0 1 1-1h10l4 4h2a1 1 0 0 1 1 1v4h-2"/><path d="M9 16h6"/><circle cx="7" cy="16.5" r="2"/><circle cx="17" cy="16.5" r="2"/>',
        'fax': '<path d="M7 9V4h10v5"/><rect x="3.5" y="9" width="17" height="8" rx="2"/><path d="M7 14h10v6H7z"/>',
        'id': '<rect x="3" y="5" width="18" height="14" rx="2"/><circle cx="9" cy="11" r="2.2"/><path d="M5.8 16c.6-1.6 1.8-2.4 3.2-2.4s2.6.8 3.2 2.4M14.5 10h4M14.5 13.5h3"/>',
        'star': '<path d="m12 3.8 2.5 5.1 5.6.8-4 4 .9 5.6L12 16.7l-5 2.6.9-5.6-4-4 5.6-.8L12 3.8Z"/>',
    }[name]
    return f'<svg class="{cls}" viewBox="0 0 24 24" aria-hidden="true" fill="none" stroke="currentColor" stroke-width="1.6" stroke-linecap="round" stroke-linejoin="round">{p}</svg>'


# ---------------------------------------------------------------------------
# Content
# ---------------------------------------------------------------------------
CARE = [
    ('hourly', 'sun', 'Hourly care', 'A few hours, when it helps most',
     'Hourly care offers you the flexibility to schedule visits when your loved one needs the most help — mornings, meals, bath time or a standing weekly visit.'),
    ('overnight', 'moon', 'Overnight care', 'A 12-hour visit through the night',
     'A caregiver stays through the night for a twelve-hour visit, so your loved one is safe and you can rest.'),
    ('live-in', 'home', '24/7 care', 'Live-in, around the clock',
     'Live-in caregivers stay in the home 24 hours a day and assist your loved one at all hours.'),
    ('specialty', 'heart', 'Specialty care', 'Dementia, Alzheimer’s and rehabilitation',
     'Our caregivers can assist your loved one with special needs, including dementia, Alzheimer’s or rehabilitation after an illness, injury or surgery.'),
]

TASKS = [
    ('Personal care', ['Bathing', 'Personal hygiene', 'Oral hygiene', 'Skin care', 'Nail care', 'Bathroom assistance']),
    ('Health support', ['Medication management and reminders', 'Vitals monitoring', 'Simple wound care', 'Catheter care', 'Home exercise program']),
    ('Everyday living', ['Companionship', 'Meal preparation', 'Light housekeeping', 'Mobility assistance and ambulation', 'Sitter services', 'General supervision and dedicated attention']),
]

WHY = [
    ('shield', 'Screened, trained caregivers', 'Every caregiver is carefully selected, background checked and supervised by licensed staff.'),
    ('card', 'Insurance or private pay', 'We accept most major insurances, which keeps out-of-pocket costs down. Call and we’ll check your plan.'),
    ('calendar', 'Flexible scheduling', 'However much or little help is needed — different times, different days — we build the schedule around your family.'),
    ('heart', '100% satisfaction guarantee', 'If you are ever unhappy with the service you receive, we will do everything we can to make it right.'),
]

REVIEWS = [
    ('We had a few scary situations with my father living at home alone after my mother passed away. We hired an hourly caregiver to come in and check on my father and make sure he is eating properly and that the house is secure. I can’t believe we didn’t do this sooner.', 'Corey L.'),
    ('We are not retired and both my husband and I have full-time jobs. We were concerned about my mother taking a fall or being lonely during the times we weren’t home. An hourly caregiver was the best decision we ever made for our peace of mind and my mother’s well-being.', 'Carol M.'),
    ('My mother needed some extra help and care around the house after her hip surgery. Rapture Ready Home Care’s caregivers have given us peace of mind and have helped my mother a great deal. I give them my highest recommendation!', 'Michael F.'),
]

# Hope at Home library. slug -> meta. Body blocks come from _src/articles.json (the old site's posts).
CATS = {
    'nurses-corner': ('Nurse’s Corner', 'Meal tips, health and medication advice, and ways to stay active — from our nursing team.'),
    'tech-savvy': ('Tech Savvy', 'Free, plain-language technology help for older adults: phones, hearing tools and telehealth.'),
    'personal-care': ('Personal Care', 'Practical advice on personal care tasks, for older adults and the people who love them.'),
    'family-support': ('Family Support', 'Guidance for family members on managing care, communicating well and caring for yourself too.'),
}
ARTICLES = [
    ('blog-stroke-recovery-guide', 'How to best support your loved one after a stroke', 'family-support', 'assets/img/caretaker.webp',
     'Recovery after a stroke unfolds gradually. Here is how families can help — with consistency, compassion and the right care approach.', 'November 5, 2025'),
    ('staying-active-and-engaged-in-onslow-county-a-guide-to-local-senior-resources', 'Staying active and engaged in Onslow County', 'nurses-corner', 'assets/img/a-senior-games.webp',
     'A guide to local senior resources — fitness, creativity and connection for Onslow County residents 65 and better.', 'February 9, 2026'),
    ('in-search-of-a-milk-alternative', 'In search of a milk alternative', 'nurses-corner', 'assets/img/a-milk-alternatives-1.webp',
     'Milk that won’t leave you bloated: how to pick the right dairy or dairy-free option for you.', 'December 17, 2025'),
    ('is-your-breakfast-cereal-healthy', 'Is your breakfast cereal healthy?', 'nurses-corner', 'assets/img/a-breakfast-rr.webp',
     'A new study looks at the nutritional value of popular breakfast cereals — maybe the one you’re eating right now.', 'December 15, 2025'),
    ('aging-tech-care-in-2026', 'Aging tech: care in 2026', 'tech-savvy', 'assets/img/a-elder-man-vrglasogon.webp',
     'Telehealth, smart monitoring and simple tools that make care at home safer — explained without the jargon.', ''),
    ('grumpy-geri-and-the-muffled-ear', 'My grandkids called me “muffled” — until I fixed my phone', 'tech-savvy', 'assets/img/a-senior-assistive-hearing-tech.webp',
     'Struggling to follow the conversation? How to make your phone do the heavy lifting for your hearing.', ''),
    ('senior-tech', 'Cell phones for seniors: a buyer’s guide', 'tech-savvy', 'assets/img/a-older-tech.webp',
     'Flip phone or smartphone? Which features matter, how to pick a plan and how to set it up so it’s easy to use.', 'September 28, 2026'),
    ('skin-care', 'Gentle glow: skincare routines after 65', 'personal-care', 'assets/img/wheelchair-care.webp',
     'Simple, effective skincare routines for every skin type — made for Onslow County’s sun and humidity.', ''),
]

# Articles rewritten from scratch (the old text was adapted from another publisher).
REWRITTEN = {
    'senior-tech': """
<p class="big">The right phone is the one you’ll actually use. Before you look at brands or prices, think about what you want the phone to do for you.</p>
<h2>Start with how you’ll use it</h2>
<ul>
<li><strong>Calls and texts only.</strong> A simple flip phone may be all you need, and it usually costs less.</li>
<li><strong>Photos and video chats with family.</strong> A smartphone makes this easy, and most can be set up with larger text and simpler screens.</li>
<li><strong>Health and safety.</strong> Look for emergency calling, fall detection, medication reminders or a way to share your location with family.</li>
</ul>
<h2>The three kinds of phones</h2>
<h3>Flip phones</h3>
<p>Real buttons, a long-lasting battery and very little to learn. Good for calling and texting. Many have large keys, loud speakers and an emergency button.</p>
<h3>Simplified smartphones</h3>
<p>Smartphones built or set up for older adults, with big icons and fewer menus. Many standard Android phones also include an “easy mode” that does the same thing.</p>
<h3>Standard smartphones</h3>
<p>An iPhone or Android phone does it all: video calls, telehealth visits, photos, maps and apps. If your family already uses iPhones, an iPhone can make sharing photos and video calls simpler.</p>
<h2>Features worth checking in the store</h2>
<ul>
<li><strong>Screen and text size.</strong> Hold the phone and read a message. Can you see it comfortably without your glasses?</li>
<li><strong>Sound and hearing.</strong> Make a test call. If you use hearing aids, look for the hearing aid compatibility (HAC) rating on the box. The <a href="https://www.fcc.gov/consumers/guides/hearing-aid-compatibility-wireless-telephones">FCC explains the ratings here</a>.</li>
<li><strong>Emergency features.</strong> Most smartphones can call 911 and alert your emergency contacts with a few button presses. Some also detect falls.</li>
<li><strong>Battery life.</strong> A phone that lasts a full day or more means fewer worries about charging.</li>
<li><strong>Buttons and grip.</strong> Make sure the buttons are easy to press and the phone doesn’t feel slippery in your hand.</li>
</ul>
<h2>Choosing a plan</h2>
<p>Plans can cost more than the phone over time, so it pays to match the plan to how you use it.</p>
<ul>
<li><strong>Talk and text only:</strong> the lowest-cost option if you don’t need the internet on your phone.</li>
<li><strong>Prepaid:</strong> pay ahead each month with no contract, and no surprise bills.</li>
<li><strong>Plans for 55 and older:</strong> several major carriers offer them. Ask exactly what’s included and whether prices change after a promotion ends.</li>
<li><strong>Coverage at home:</strong> check each carrier’s coverage map for your own address before you sign up, and ask neighbors which service works well for them.</li>
</ul>
<p>Bring a family member or friend along when you shop, and ask the store to transfer your contacts and photos before you leave.</p>
<h2>Set it up to be easy to use</h2>
<ul>
<li>Make the text and icons larger in the phone’s display settings.</li>
<li>Turn on live captions for calls and videos if hearing is a challenge.</li>
<li>Add emergency contacts and your medical information so first responders can see it.</li>
<li>Put the people you call most on the home screen as favorites.</li>
<li>Turn on spam call filtering to cut down on unwanted calls.</li>
</ul>
<h2>Stay safe from phone scams</h2>
<ul>
<li>Never share a code that was texted to you with someone who calls or texts asking for it.</li>
<li>Medicare, Social Security and your bank won’t call to demand payment or gift cards.</li>
<li>If a call feels urgent or frightening, hang up and call back using a number you already know.</li>
</ul>
<h2>We’re happy to help</h2>
<p>Rapture Ready Home Care offers free technology advice and training for older adults through <a href="https://cyberseniors.org/">Cyber-Seniors</a>. Our caregivers can also help your loved one practice calls, texts and video chats at home. Call us at 1 (252) 503-2978 to learn more.</p>
""",
}

# Fact-check fixes applied to the old article text: Rapture Ready did not test phones or carriers,
# so first-person testing claims are reworded to point at the linked outside reviews.
FIXUPS = [
    ('From budget-friendly phones to feature-packed smartphones—we’ve done the research to help you find the right device at the right price. You can also explore our latest carrier reviews to see how today’s top providers stack up for seniors, plus detailed pricing guides to help you score the best deals. If you’re stuck choosing between carriers, we’ve tested and compared them so you don’t have to.',
     'From budget-friendly phones to feature-packed smartphones and simple flip phones, the independent reviews linked below can help you find the right device at the right price.'),
    ('From budget-friendly phones to feature-packed smartphones—and even simple flip phones—we’ve done the research to help you find the right device at the right price. You can also explore our latest carrier reviews to see how today’s top providers stack up for seniors, plus detailed pricing guides to help you score the best deals. If you’re stuck choosing between carriers, we’ve tested and compared them so you don’t have to.',
     'From budget-friendly phones to feature-packed smartphones and simple flip phones, the independent reviews linked below can help you find the right device at the right price.'),
    ('Our Latest Cell Phone Carrier Reviews', 'Independent carrier reviews'),
]

COMMUNITY = [
    ('Onslow County Senior Services', 'Programs, classes and support services for older adults.', 'https://www.onslowcountync.gov/538/Senior-Services'),
    ('Onslow County Senior Center', 'Activities, trips and social events close to home.', 'https://www.onslowcountync.gov/591/Senior-Center'),
    ('Living Healthy With Diabetes', 'A free county workshop for managing diabetes day to day.', 'https://www.onslowcountync.gov/624/Living-Healthy-With-Diabetes'),
]


# ---------------------------------------------------------------------------
# Page shell
# ---------------------------------------------------------------------------
NAV = [('about-us', 'About'), ('our-services', 'Services'), ('hope-at-home', 'Hope at Home'), ('contact-us', 'Contact')]


class Page:
    def __init__(self, slug):
        self.slug = slug
        self.depth = 0 if slug == '' else slug.count('/') + 1

    def u(self, path):
        """Relative URL from this page to a site path ('' = home, 'assets/x', 'about-us')."""
        pre = '../' * self.depth
        if path == '':
            return pre or './'
        if path.startswith(('http', 'mailto:', 'tel:', '#')):
            return path
        if path.startswith('assets/') or '.' in path.split('/')[-1] or '#' in path:
            if '#' in path and not path.startswith('assets/'):
                p, h = path.split('#', 1)
                return (pre + (p + '/' if p else '') or './') + '#' + h
            return pre + path
        return pre + path + '/'


def phone_link(cls='', label=None):
    return f'<a class="{cls}" href="tel:{B["tel"]}">{icon("phone")}<span>{label or B["phone"]}</span></a>'


def shell(pg, title, desc, body, active=None, og_img='assets/img/hero-care.webp'):
    canonical = DOMAIN + '/' + (pg.slug + '/' if pg.slug else '')
    nav = ''.join(
        f'<li><a href="{pg.u(s)}"{" aria-current=page" if active == s else ""}>{t}</a></li>' for s, t in NAV)
    return f'''<!doctype html>
<!-- Built by Truly Digital Solutions, LLC (TruTech) · https://trutech.us · Build {BUILD_ID} -->
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="author" content="Truly Digital Solutions, LLC (TruTech)">
<meta name="generator" content="TruTech · trutech.us">
<meta name="trutech-build" content="{BUILD_ID}">
<title>{esc(title)}</title>
<meta name="description" content="{esc(desc)}">
<link rel="canonical" href="{canonical}">
<meta property="og:type" content="website">
<meta property="og:title" content="{esc(title)}">
<meta property="og:description" content="{esc(desc)}">
<meta property="og:url" content="{canonical}">
<meta property="og:image" content="{DOMAIN}/{og_img}">
<meta name="theme-color" content="#7a1c2a">
<link rel="icon" href="{pg.u('assets/img/favicon.png')}">
<link rel="apple-touch-icon" href="{pg.u('assets/img/apple-touch-icon.png')}">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible+Next:ital,wght@0,400;0,600;0,700;1,400&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,500;0,6..72,600;1,6..72,400;1,6..72,500&display=swap">
<link rel="stylesheet" href="{pg.u('assets/site.css')}">
<script>try{{var s=localStorage.getItem('rr-size');if(s)document.documentElement.dataset.size=s}}catch(e){{}}</script>
<script src="{pg.u('assets/site.js')}" defer></script>
{schema(pg) if pg.slug == '' else ''}
</head>
<body>
<a class="skip" href="#main">Skip to main content</a>
<div class="util">
  <div class="wrap util__in">
    <p class="util__status" data-status><span class="dot" aria-hidden="true"></span><span data-status-text>Office hours: {B['hours_short']}</span></p>
    <div class="util__right">
      <div class="size" role="group" aria-label="Text size">
        <span class="size__label">Text size</span>
        <button type="button" data-size-btn="1" aria-pressed="true" aria-label="Normal text">A</button>
        <button type="button" data-size-btn="2" aria-pressed="false" aria-label="Larger text">A</button>
        <button type="button" data-size-btn="3" aria-pressed="false" aria-label="Largest text">A</button>
      </div>
      {phone_link('util__phone')}
    </div>
  </div>
</div>
<header class="hdr" data-hdr>
  <div class="wrap hdr__in">
    <a class="brand" href="{pg.u('')}" aria-label="Rapture Ready Home Care, home">
      <img src="{pg.u('assets/img/logo-full.webp')}" alt="" width="104" height="82">
      <span class="brand__name">Rapture Ready<br><em>Home Care</em></span>
    </a>
    <nav class="nav" aria-label="Main" data-nav>
      <ul>{nav}</ul>
      <a class="btn btn--primary nav__cta" href="{pg.u('request-care')}">Request care</a>
      <a class="nav__phone" href="tel:{B['tel']}">{icon('phone')}{B['phone']}</a>
    </nav>
    <button class="menu-btn" type="button" aria-expanded="false" aria-controls="menu" data-menu-btn><span class="menu-btn__bars" aria-hidden="true"></span><span data-menu-label>Menu</span></button>
  </div>
</header>
<main id="main">
{body}
</main>
{footer(pg)}
</body>
</html>
'''


def schema(pg):
    data = {
        '@context': 'https://schema.org', '@type': 'HomeHealthCareService',
        'name': B['name'], 'url': DOMAIN + '/', 'telephone': '+1-252-503-2978', 'faxNumber': '+1-910-333-0128',
        'email': B['email'], 'image': DOMAIN + '/assets/img/hero-care.webp', 'logo': DOMAIN + '/assets/img/logo-full.png',
        'address': {'@type': 'PostalAddress', 'streetAddress': '625 College St.', 'addressLocality': 'Jacksonville',
                    'addressRegion': 'NC', 'postalCode': '28540', 'addressCountry': 'US'},
        'areaServed': 'Jacksonville, NC and Eastern North Carolina',
        'openingHoursSpecification': [{'@type': 'OpeningHoursSpecification',
                                       'dayOfWeek': ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday'],
                                       'opens': '09:00', 'closes': '17:00'}],
        'identifier': {'@type': 'PropertyValue', 'propertyID': 'NPI', 'value': B['npi']},
    }
    return f'<script type="application/ld+json">{json.dumps(data)}</script>'


def footer(pg):
    return f'''<footer class="ftr">
  <div class="wrap ftr__grid">
    <div class="ftr__about">
      <a class="brand brand--ftr" href="{pg.u('')}"><img src="{pg.u('assets/img/logo-full.webp')}" alt="" width="104" height="82"><span class="brand__name">Rapture Ready<br><em>Home Care</em></span></a>
      <p>In-home companions and caregivers for seniors and adults in and around Jacksonville, NC — so the people you love can live well in their own home.</p>
    </div>
    <div>
      <h2 class="ftr__h">Visit or call</h2>
      <ul class="ftr__list">
        <li>{icon('pin')}<a href="{B['map']}" target="_blank" rel="noopener">{B['street']}<br>{B['city']}</a></li>
        <li>{icon('phone')}<a href="tel:{B['tel']}">{B['phone']}</a></li>
        <li>{icon('fax')}<span>Fax {B['fax']}</span></li>
        <li>{icon('mail')}<a href="mailto:{B['email']}">{B['email']}</a></li>
      </ul>
    </div>
    <div>
      <h2 class="ftr__h">Office hours</h2>
      <ul class="ftr__list">
        <li>{icon('clock')}<span>Monday – Friday<br>9:00 am – 5:00 pm</span></li>
        <li class="muted-li"><span>Saturday and Sunday closed</span></li>
        <li>{icon('id')}<span>NPI {B['npi']}<br><small>For insurance use</small></span></li>
      </ul>
    </div>
    <div>
      <h2 class="ftr__h">Explore</h2>
      <ul class="ftr__links">
        <li><a href="{pg.u('request-care')}">Request care</a></li>
        <li><a href="{pg.u('our-services')}">Our services</a></li>
        <li><a href="{pg.u('about-us')}">About us</a></li>
        <li><a href="{pg.u('hope-at-home')}">Hope at Home</a></li>
        <li><a href="{pg.u('contact-us')}">Contact us</a></li>
        <li><a href="{B['sister']}" target="_blank" rel="noopener">Faithful Rides (transportation)</a></li>
      </ul>
    </div>
  </div>
  <div class="wrap ftr__legal">
    <p>© <span data-year>{date.today().year}</span> Rapture Ready Home Care. All rights reserved.</p>
    <p><a href="{pg.u('privacy-policy')}">Privacy policy</a> <span aria-hidden="true">/</span> Site by <a href="https://trutech.us" target="_blank" rel="noopener">TruTech</a></p>
  </div>
</footer>'''


# ---------------------------------------------------------------------------
# Reusable sections
# ---------------------------------------------------------------------------
def page_head(title, lead, crumb=None, pg=None, img=None):
    crumbs = ''
    if crumb and pg:
        crumbs = f'<p class="crumb"><a href="{pg.u(crumb[0])}">{icon("back")}{crumb[1]}</a></p>'
    art = f'<div class="phead__img arch"><img src="{pg.u(img)}" alt="" loading="eager"></div>' if img else ''
    return f'''<section class="phead{' phead--img' if img else ''}">
  <div class="wrap phead__in">
    <div class="phead__txt">{crumbs}<h1>{title}</h1><p class="lead">{lead}</p></div>{art}
  </div>
</section>'''


def cta_band(pg, title='Talk with us about care', text='Tell us a little about your loved one. We’ll talk through schedules, insurance or private pay, and what help at home could look like.'):
    return f'''<section class="band">
  <div class="wrap band__in">
    <div><h2>{title}</h2><p>{text}</p></div>
    <div class="band__actions">
      <a class="btn btn--light" href="{pg.u('request-care')}">Request care</a>
      <a class="btn btn--ghost-light" href="tel:{B['tel']}">{icon('phone')}Call {B['phone']}</a>
    </div>
  </div>
</section>'''


def why_list():
    items = ''.join(f'<li>{icon(i)}<div><h3>{t}</h3><p>{d}</p></div></li>' for i, t, d in WHY)
    return f'<ul class="why">{items}</ul>'


def care_grid(pg, detailed=False):
    rows = ''
    for key, ic, t, sub, d in CARE:
        rows += f'''<li class="care__item" id="{key}">
      <span class="care__ic">{icon(ic)}</span>
      <h3>{t}</h3>
      <p class="care__sub">{sub}</p>
      <p>{d}</p>
    </li>'''
    return f'<ul class="care">{rows}</ul>'


def task_cols():
    cols = ''
    for t, items in TASKS:
        lis = ''.join(f'<li>{icon("check")}{x}</li>' for x in items)
        cols += f'<div class="tasks__col"><h3>{t}</h3><ul>{lis}</ul></div>'
    return f'<div class="tasks">{cols}</div>'


def reviews():
    qs = ''.join(f'''<figure class="quote">
      <div class="stars" aria-label="5 out of 5 stars">{icon('star','st')*5}</div>
      <blockquote><p>“{q}”</p></blockquote>
      <figcaption>{n}</figcaption>
    </figure>''' for q, n in REVIEWS)
    return f'<div class="quotes">{qs}</div>'


def director(pg, full=False):
    return f'''<section class="sec director">
  <div class="wrap director__in">
    <div class="director__img arch"><img src="{pg.u('assets/img/director.webp')}" alt="Latasia Bowman, RN, Agency Director, smiling in purple scrubs" loading="lazy" width="640" height="800"></div>
    <div class="director__txt">
      <h2>Hearts that serve</h2>
      <p class="pull">“Where compassion meets calling — and care becomes a ministry of excellence.”</p>
      <p>At Rapture Ready Home Care, every act of service is guided by both heart and purpose. Our caregivers don’t just provide assistance; they answer a calling to serve with grace, skill and unwavering dedication. Compassion fuels our care — professionalism defines our standard.</p>
      <div class="sig">
        <p class="sig__name">Latasia Bowman, RN</p>
        <p class="sig__role">Agency Director <br>Infusion trained, graduate of ECU</p>
      </div>
    </div>
  </div>
</section>'''


def article_cards(pg, items):
    out = ''
    for slug, title, cat, img, dek, dt in items:
        out += f'''<article class="acard">
      <a href="{pg.u(slug)}" class="acard__link">
        <div class="acard__img"><img src="{pg.u(img)}" alt="" loading="lazy"></div>
        <p class="acard__cat">{CATS[cat][0]}</p>
        <h3>{title}</h3>
        <p>{dek}</p>
      </a>
    </article>'''
    return f'<div class="acards">{out}</div>'


def contact_block(pg, heading='Send us a message', intro=True):
    return f'''<div class="contact">
  <div class="contact__info">
    <h2>{heading}</h2>
    {'<p>Call during office hours to talk with our team right away, or send a message and we’ll call you back.</p>' if intro else ''}
    <ul class="clist">
      <li>{icon('phone')}<div><p class="clist__k">Phone</p><a href="tel:{B['tel']}">{B['phone']}</a></div></li>
      <li>{icon('mail')}<div><p class="clist__k">Email</p><a href="mailto:{B['email']}">{B['email']}</a></div></li>
      <li>{icon('pin')}<div><p class="clist__k">Office</p><a href="{B['map']}" target="_blank" rel="noopener">{B['street']}, {B['city']}</a></div></li>
      <li>{icon('clock')}<div><p class="clist__k">Office hours</p><p>{B['hours']}<br>Saturday and Sunday closed</p></div></li>
      <li>{icon('id')}<div><p class="clist__k">NPI (for insurance use)</p><p>{B['npi']}</p></div></li>
    </ul>
  </div>
  {care_form(pg)}
</div>'''


def care_form(pg, full=False):
    care_opts = ''.join(f'<option>{t}</option>' for _, _, t, _, _ in CARE) + '<option>Not sure yet</option>'
    extra = ''
    if full:
        extra = f'''
    <div class="field"><label for="f-who">Who needs care?</label>
      <select id="f-who" name="who"><option>A parent</option><option>A spouse or partner</option><option>Myself</option><option>Another family member or friend</option></select></div>
    <div class="field"><label for="f-care">Type of care</label><select id="f-care" name="care">{care_opts}</select></div>
    <div class="field"><label for="f-start">When would you like care to start?</label>
      <select id="f-start" name="start"><option>As soon as possible</option><option>Within a few weeks</option><option>I’m planning ahead</option></select></div>
    <fieldset class="field"><legend>How will care be paid for?</legend>
      <div class="radios">
        <label><input type="radio" name="pay" value="Insurance" checked> Insurance</label>
        <label><input type="radio" name="pay" value="Private pay"> Private pay</label>
        <label><input type="radio" name="pay" value="Not sure"> Not sure</label>
      </div></fieldset>'''
    return f'''<form class="form" data-form data-subject="{'Care request' if full else 'Website message'}" data-email="{B['email']}" novalidate>
    <div class="field"><label for="f-name">Your name <span class="req">(required)</span></label><input id="f-name" name="name" autocomplete="name" required></div>
    <div class="field"><label for="f-phone">Phone number <span class="req">(required)</span></label><input id="f-phone" name="phone" type="tel" autocomplete="tel" required></div>
    <div class="field"><label for="f-email">Email</label><input id="f-email" name="email" type="email" autocomplete="email"></div>{extra}
    <div class="field"><label for="f-msg">{'Tell us about your loved one’s needs' if full else 'Your message'}</label><textarea id="f-msg" name="message" rows="4"></textarea></div>
    <p class="form__err" role="alert" data-form-err></p>
    <button class="btn btn--primary btn--block" type="submit">{'Send care request' if full else 'Send message'}</button>
    <p class="form__note">This opens your email app with your details filled in, ready to send. Please don’t include medical records — we’ll talk through details by phone.</p>
  </form>'''


# ---------------------------------------------------------------------------
# Pages
# ---------------------------------------------------------------------------
def home():
    pg = Page('')
    latest = [a for a in ARTICLES if a[0] in ('blog-stroke-recovery-guide', 'staying-active-and-engaged-in-onslow-county-a-guide-to-local-senior-resources', 'grumpy-geri-and-the-muffled-ear')]
    comm = ''.join(f'<li><a href="{h}" target="_blank" rel="noopener"><span class="comm__t">{t}</span><span class="comm__d">{d}</span></a></li>' for t, d, h in COMMUNITY)
    body = f'''
<section class="hero">
  <div class="wrap hero__in">
    <div class="hero__txt">
      <p class="hero__kicker">In-home care in Jacksonville and Eastern North Carolina</p>
      <h1>You can’t always be there. But we can.</h1>
      <p class="lead">Rapture Ready Home Care sends trained, screened caregivers into your loved one’s home — for a few hours, overnight or around the clock — so they can live well, safely, where they’re most comfortable.</p>
      <div class="hero__actions">
        <a class="btn btn--primary btn--lg" href="{pg.u('request-care')}">Request care</a>
        <a class="btn btn--outline btn--lg" href="tel:{B['tel']}">{icon('phone')}Call {B['phone']}</a>
      </div>
      <ul class="hero__facts">
        <li>{icon('card')}Most major insurances and private pay</li>
        <li>{icon('shield')}Background-checked caregivers</li>
      </ul>
    </div>
    <div class="hero__art">
      <div class="arch hero__photo"><img src="{pg.u('assets/img/hero-care.webp')}" alt="A Rapture Ready caregiver holding hands with a smiling older woman on her sofa" width="853" height="1067" fetchpriority="high"></div>
      <div class="hero__badge">
        <img src="{pg.u('assets/img/director.webp')}" alt="" width="64" height="80">
        <p><strong>Led by Latasia Bowman, RN</strong><span>Agency Director</span></p>
      </div>
    </div>
  </div>
</section>

<section class="sec sec--tight">
  <div class="wrap">{why_list()}</div>
</section>

<section class="sec sec--blush" id="care">
  <div class="wrap">
    <div class="sec__head">
      <h2>Care that fits the hours you need</h2>
      <p>From a morning visit to a caregiver who lives in, choose the level of help that fits your loved one today — and change it as needs change.</p>
    </div>
    {care_grid(pg)}
  </div>
</section>

<section class="sec">
  <div class="wrap split">
    <div class="split__img"><img src="{pg.u('assets/img/cane-help.webp')}" alt="A caregiver in blue scrubs helping an older woman stand up from her sofa with her cane" loading="lazy" width="1400" height="933"></div>
    <div class="split__txt">
      <h2>What our caregivers help with</h2>
      <p>Everyday help that keeps your loved one safe, clean, fed and connected — with the right balance of independence, dignity and quality of life.</p>
      <a class="textlink" href="{pg.u('our-services')}">See all services{icon('arrow')}</a>
    </div>
  </div>
  <div class="wrap">{task_cols()}</div>
</section>

{director(pg)}

<section class="sec sec--blush">
  <div class="wrap">
    <div class="sec__head">
      <h2>What families say</h2>
      <p>Peace of mind is what we hear about most.</p>
    </div>
    {reviews()}
  </div>
</section>

<section class="sec">
  <div class="wrap">
    <div class="sec__head">
      <h2>Getting started is simple</h2>
    </div>
    <ol class="steps">
      <li><h3>Reach out</h3><p>Call {B['phone']} during office hours or send a care request any time.</p></li>
      <li><h3>Talk it through</h3><p>Tell us what your loved one needs, the hours that help most, and whether you’ll use insurance or private pay.</p></li>
      <li><h3>Care begins at home</h3><p>We set up a caregiver schedule that fits — and adjust it whenever your family’s needs change.</p></li>
    </ol>
  </div>
</section>

<section class="sec sec--line">
  <div class="wrap">
    <div class="sec__head sec__head--row">
      <div><h2>Hope at Home</h2><p>Free advice for older adults and their families from our nurses and caregivers.</p></div>
      <a class="textlink" href="{pg.u('hope-at-home')}">Read all articles{icon('arrow')}</a>
    </div>
    {article_cards(pg, latest)}
  </div>
</section>

<section class="sec sec--blush">
  <div class="wrap comm">
    <div class="comm__intro">
      <h2>Staying connected in Onslow County</h2>
      <p>Social time matters as much as care. These county programs help seniors stay active, informed and involved.</p>
    </div>
    <ul class="comm__list">{comm}</ul>
  </div>
</section>

<section class="sec" id="contact">
  <div class="wrap">{contact_block(pg, 'Want to learn more?')}</div>
</section>

<section class="sister">
  <div class="wrap sister__in">
    {icon('van')}
    <p><strong>Need a ride to an appointment?</strong> Our sister company, Faithful Rides, provides non-emergency medical transportation from the same College Street office.</p>
    <a class="textlink" href="{B['sister']}" target="_blank" rel="noopener">Visit Faithful Rides{icon('arrow')}</a>
  </div>
</section>
'''
    return pg, shell(pg, 'In-Home Care in Jacksonville, NC | Rapture Ready Home Care',
                     'Trusted in-home care for seniors and adults in Jacksonville, NC: hourly, overnight, 24/7 live-in and dementia care from screened, trained caregivers. Most insurances accepted.', body)


def about():
    pg = Page('about-us')
    body = page_head('Care at home, with dignity',
                     'Rapture Ready Home Care provides quality in-home care to seniors and adults in and around Jacksonville, NC, so they can live happier, healthier and fuller lives in the comfort of their own home.',
                     pg=pg, img='assets/img/kitchen.webp') + f'''
<section class="sec">
  <div class="wrap prose-2">
    <div>
      <h2>Why we do this work</h2>
    </div>
    <div class="prose">
      <p class="big">We believe every adult deserves the right to live in the comfort of their own home with dignity.</p>
      <p>That’s why we aim to give every family peace of mind — knowing we’ll treat their loved one with the care and respect they deserve. When you hire people to care for someone you love, you want people you can trust and who provide top-rate care. That is exactly our specialty.</p>
      <p>Our in-home care balances independence, dignity and quality of life while keeping your loved one safe. Rapture Ready caregivers receive thorough training, ongoing support and the resources they need to deliver a care experience you can count on.</p>
    </div>
  </div>
</section>
{director(pg)}
<section class="sec">
  <div class="wrap">
    <div class="sec__head"><h2>Why families choose us</h2></div>
    {why_list()}
  </div>
</section>
<section class="sec sec--blush">
  <div class="wrap split split--rev">
    <div class="split__img"><img src="{pg.u('assets/img/hug.webp')}" alt="An older woman smiling as a younger woman hugs her from behind on a sofa" loading="lazy" width="1400" height="1090"></div>
    <div class="split__txt">
      <h2>Let us treat your loved ones like family</h2>
      <p>You can’t always be there. Our dedicated caregivers are ready to make your life easier by providing quality care and assistance for your loved one at home.</p>
      <p>And when a trip to the doctor is part of the day, our sister company <a href="{B['sister']}" target="_blank" rel="noopener">Faithful Rides</a> can provide the transportation.</p>
    </div>
  </div>
</section>
{cta_band(pg)}'''
    return pg, shell(pg, 'About Us | Rapture Ready Home Care, Jacksonville NC',
                     'Meet Rapture Ready Home Care: Jacksonville’s in-home care team for seniors and adults, led by Agency Director Latasia Bowman, RN.', body, 'about-us', 'assets/img/director.webp')


def services():
    pg = Page('our-services')
    faq = [
        ('What areas do you serve?', 'We care for seniors and adults in Jacksonville, NC and surrounding communities in Eastern North Carolina. Call us to confirm your address is in our service area.'),
        ('Do you accept insurance?', f'Yes. We accept most major insurances, and private pay is welcome too. Call {B["phone"]} and we’ll help you check your plan. Our NPI for insurance use is {B["npi"]}.'),
        ('Can a caregiver help someone living with dementia?', 'Yes. Our specialty care supports loved ones with dementia and Alzheimer’s, as well as people in rehabilitation after an illness, injury or surgery.'),
        ('How long is an overnight visit?', 'Overnight care is a twelve-hour visit. If your loved one needs someone at all hours, ask about 24/7 live-in care.'),
        ('Can you help with rides to appointments?', f'Transfer assistance and non-emergency medical transportation are provided through our sister company, <a href="{B["sister"]}" target="_blank" rel="noopener">Faithful Rides</a>.'),
        ('What happens if we’re not happy with the care?', 'Tell us. We offer a 100% satisfaction guarantee and will do everything we can to make it right.'),
    ]
    faq_html = ''.join(f'<details class="faq__item"><summary>{q}<span class="faq__plus" aria-hidden="true"></span></summary><div class="faq__a"><p>{a}</p></div></details>' for q, a in faq)
    body = page_head('Our services',
                     'Quality senior and adult home care and companionship from compassionate, trained caregivers — from a few hours a week to around-the-clock support.',
                     pg=pg, img='assets/img/nurse-visit.webp') + f'''
<section class="sec">
  <div class="wrap">
    <div class="sec__head"><h2>Choose the level of care</h2><p>Our in-home aides and companions help adults, seniors and elderly loved ones with daily living, in the comfort of their own home. Their safety and wellness is our top priority.</p></div>
    {care_grid(pg, True)}
  </div>
</section>
<section class="sec sec--blush">
  <div class="wrap">
    <div class="sec__head"><h2>Everything our caregivers can help with</h2><p>Including, but not limited to:</p></div>
    {task_cols()}
  </div>
</section>
<section class="sec">
  <div class="wrap split">
    <div class="split__img"><img src="{pg.u('assets/img/wheelchair-care.webp')}" alt="A caregiver kneeling to help an older man in a wheelchair at home" loading="lazy" width="1200" height="799"></div>
    <div class="split__txt">
      <h2>Paying for care</h2>
      <p>We accept most major insurances, which minimizes your out-of-pocket expenses. Private pay is welcome too.</p>
      <dl class="npi"><dt>NPI for insurance use</dt><dd>{B['npi']}</dd></dl>
      <p>Not sure what your plan covers? Call {B['phone']} and we’ll walk through it with you.</p>
    </div>
  </div>
</section>
<section class="sec sec--line">
  <div class="wrap faq">
    <h2>Common questions</h2>
    <div class="faq__list">{faq_html}</div>
  </div>
</section>
{cta_band(pg)}'''
    return pg, shell(pg, 'Home Care Services in Jacksonville, NC | Rapture Ready Home Care',
                     'Hourly, overnight, 24/7 live-in and specialty dementia and rehabilitation care at home in Jacksonville, NC. Personal care, meals, medication reminders, companionship and more.', body, 'our-services', 'assets/img/cane-help.webp')


def request_care():
    pg = Page('request-care')
    body = page_head('Request care',
                     'Tell us about your loved one and we’ll call you back to talk through care, scheduling and insurance or private pay.', pg=pg) + f'''
<section class="sec sec--flush">
  <div class="wrap reqpage">
    <div class="req__form">{care_form(pg, True)}</div>
    <aside class="req__aside">
      <div class="req__card">
        <h2>Prefer to talk?</h2>
        <p>Call during office hours and speak with our team directly.</p>
        <a class="btn btn--primary btn--block" href="tel:{B['tel']}">{icon('phone')}{B['phone']}</a>
        <p class="req__hours">{B['hours']}</p>
      </div>
      <div class="req__card req__card--quiet">
        <h2>What happens next</h2>
        <ol class="mini-steps"><li>We call you back to learn about your loved one’s needs.</li><li>We talk through hours, insurance or private pay.</li><li>We set up a caregiver schedule that fits.</li></ol>
      </div>
      <p class="req__911">In a medical emergency, call 911.</p>
    </aside>
  </div>
</section>'''
    return pg, shell(pg, 'Request Care | Rapture Ready Home Care, Jacksonville NC',
                     'Request in-home care for a parent or loved one in Jacksonville, NC. Tell us what they need and we’ll call you back.', body, None)


def contact():
    pg = Page('contact-us')
    body = page_head('Contact us', 'We’re here to answer your questions about in-home care — for yourself or someone you love.', pg=pg) + f'''
<section class="sec sec--flush">
  <div class="wrap">{contact_block(pg, 'Reach our office', False)}</div>
</section>
<section class="mapwrap">
  <iframe title="Map of 625 College St., Jacksonville, NC" src="https://maps.google.com/maps?q=625+College+St.,+Jacksonville,+NC+28540&z=15&output=embed" loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
</section>'''
    return pg, shell(pg, 'Contact Us | Rapture Ready Home Care, Jacksonville NC',
                     f'Call {B["phone"]}, email {B["email"]} or visit 625 College St., Jacksonville, NC 28540. Office hours Monday–Friday, 9 am–5 pm.', body, 'contact-us')


def hope():
    pg = Page('hope-at-home')
    cats = ''
    for key, (t, d) in CATS.items():
        n = sum(1 for a in ARTICLES if a[2] == key)
        cats += f'<li><a href="{pg.u(key)}"><span class="cat__t">{t}</span><span class="cat__d">{d}</span><span class="cat__n">{n} article{"s" if n != 1 else ""}</span></a></li>'
    body = page_head('Hope at Home',
                     'Hands that heal, hearts that serve. General health tips, news and stories of faith and service — for family members, caregivers and friends. May you find comfort, inspiration and hope in every word.',
                     pg=pg, img='assets/img/companions.webp') + f'''
<section class="sec sec--flush">
  <div class="wrap">
    <ul class="cats">{cats}</ul>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="sec__head"><h2>All articles</h2></div>
    {article_cards(pg, ARTICLES)}
  </div>
</section>
{cta_band(pg, 'Questions about care at home?')}'''
    return pg, shell(pg, 'Hope at Home | Senior Care Tips & Resources | Rapture Ready Home Care',
                     'Free advice for older adults and families in Onslow County: nutrition, staying active, technology help, personal care and family caregiving support.', body, 'hope-at-home', 'assets/img/companions.webp')


def category(key):
    pg = Page(key)
    t, d = CATS[key]
    items = [a for a in ARTICLES if a[2] == key]
    extra = ''
    if key == 'tech-savvy':
        extra = '<p class="note">Rapture Ready Home Care provides free technology advice and training for older adults through Cyber-Seniors. Ask us about it when you call.</p>'
    body = page_head(t, d, crumb=('hope-at-home', 'Hope at Home'), pg=pg) + f'''
<section class="sec sec--flush">
  <div class="wrap">{extra}{article_cards(pg, items)}</div>
</section>
{cta_band(pg, 'Questions about care at home?')}'''
    return pg, shell(pg, f'{t} | Hope at Home | Rapture Ready Home Care', d, body, 'hope-at-home')


def alias(slug, target, title):
    """Old hub URLs (get-active, nutrition-blog) now point at their category."""
    pg = Page(slug)
    href = pg.u(target)
    return pg, f'''<!doctype html>
<!-- Built by Truly Digital Solutions, LLC (TruTech) · https://trutech.us · Build {BUILD_ID} -->
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<meta name="trutech-build" content="{BUILD_ID}"><title>{title} | Rapture Ready Home Care</title>
<link rel="canonical" href="{DOMAIN}/{target}/"><meta http-equiv="refresh" content="0; url={href}"></head>
<body><p>This page has moved to <a href="{href}">{title}</a>.</p></body></html>'''


def render_blocks(pg, blocks, skip_title):
    out, i, in_list = [], 0, False
    rows = []
    dropped_title = False
    def close_list():
        nonlocal in_list
        if in_list: out.append('</ul>'); in_list = False
    def close_table():
        nonlocal rows
        if rows:
            head, *rest = rows
            th = ''.join(f'<th scope="col">{c}</th>' for c in head)
            trs = ''.join('<tr>' + ''.join(f'<td>{c}</td>' for c in r) + '</tr>' for r in rest)
            out.append(f'<div class="tablewrap"><table><thead><tr>{th}</tr></thead><tbody>{trs}</tbody></table></div>')
            rows = []
    for b in blocks:
        kind = b[0]
        if kind != 'tr': close_table()
        if kind != 'li': close_list()
        if kind in ('img', 'bg'):
            continue  # images placed separately (hero) to keep pages calm; inline ones handled below
        txt = b[1]
        txt = re.sub(r'href="@@([^"]*)"', lambda m: f'href="{pg.u(m.group(1).strip("/"))}"', txt)
        plain = re.sub(r'<[^>]+>', '', txt).strip()
        if plain.lower() in ('learn more', 'read more'):
            continue
        if re.fullmatch(r'[A-Za-z]{3,9}\.? \d{1,2}(st|nd|rd|th)?,? \d{4}', plain) or re.fullmatch(r'\d+ Resources', plain):
            continue  # dates live in the header; "N Resources" was an old widget label
        for bad, good in FIXUPS:
            txt = txt.replace(bad, good)
        if not txt.strip():
            continue
        if not dropped_title and kind == 'h2' and plain.lower().rstrip('?.!') in skip_title:
            dropped_title = True; continue
        if kind == 'h2':
            out.append(f'<h2>{txt}</h2>')
        elif kind == 'h3':
            out.append(f'<p class="big">{txt}</p>' if len(plain) > 90 else f'<h3>{txt}</h3>')
        elif kind == 'li':
            if not in_list: out.append('<ul>'); in_list = True
            out.append(f'<li>{txt}</li>')
        elif kind == 'tr':
            rows.append(b[1])
        else:
            if re.fullmatch(r'<em>[A-Za-z]{3,9}\.? \d{1,2}(st|nd|rd|th)?,? \d{4}</em>', txt.strip()):
                continue  # dates shown in the header instead
            out.append(f'<p>{txt}</p>')
    close_list(); close_table()
    return '\n'.join(out)


def article(meta, data):
    slug, title, cat, img, dek, dt = meta
    pg = Page(slug)
    blocks = data['blocks']
    skip = {title.lower().rstrip('?.!')}
    first_h2 = next((re.sub(r'<[^>]+>', '', b[1]) for b in blocks if b[0] == 'h2'), '')
    skip.add(first_h2.lower().rstrip('?.!'))
    # Inline figures: keep the article's own images (charts, guides, phones) as a gallery at the end.
    figs = [] if slug in REWRITTEN else [b for b in blocks if b[0] == 'img' and b[1] != img]
    gallery = ''
    if figs:
        gallery = '<div class="gallery">' + ''.join(
            f'<figure><img src="{pg.u(f[1])}" alt="{esc(f[2] or "")}" loading="lazy" width="{f[3]}" height="{f[4]}"></figure>' for f in figs) + '</div>'
    content = REWRITTEN.get(slug) or render_blocks(pg, blocks, skip)
    related = [a for a in ARTICLES if a[2] == cat and a[0] != slug][:2] or [a for a in ARTICLES if a[0] != slug][:2]
    body = f'''
<article class="post">
  <header class="post__head wrap">
    <p class="crumb"><a href="{pg.u(cat)}">{icon('back')}{CATS[cat][0]}</a></p>
    <h1>{title}</h1>
    <p class="lead">{dek}</p>
    {f'<p class="post__date">{dt}</p>' if dt else ''}
  </header>
  <div class="post__hero wrap"><img src="{pg.u(img)}" alt="" width="1200" height="800"></div>
  <div class="post__body wrap-narrow prose">
    {content}
    {gallery}
    <aside class="post__cta">
      <p><strong>Rapture Ready Home Care</strong> provides in-home care for seniors and adults in and around Jacksonville, NC.</p>
      <p><a class="btn btn--primary" href="{pg.u('request-care')}">Request care</a> <a class="btn btn--outline" href="tel:{B['tel']}">{icon('phone')}{B['phone']}</a></p>
    </aside>
  </div>
</article>
<section class="sec sec--line">
  <div class="wrap">
    <div class="sec__head sec__head--row"><h2>Keep reading</h2><a class="textlink" href="{pg.u('hope-at-home')}">All articles{icon('arrow')}</a></div>
    {article_cards(pg, related)}
  </div>
</section>'''
    return pg, shell(pg, f'{title} | Rapture Ready Home Care', dek, body, 'hope-at-home', img)


def privacy():
    pg = Page('privacy-policy')
    body = page_head('Privacy policy', 'How this website handles your information. Last updated September 28, 2026.', pg=pg) + f'''
<section class="sec sec--flush">
  <div class="wrap-narrow prose">
    <h2>What we collect</h2>
    <p>This website does not collect personal information on its own. When you use our contact or care request forms, your details (such as your name, phone number and email) are placed into an email in your own email app. Nothing is sent until you choose to send that email to {B['email']}.</p>
    <p>If you call, email or send us a message, we use what you share only to respond to you and to arrange care.</p>
    <h2>Cookies and tracking</h2>
    <p>This website does not use advertising or tracking cookies. If you change the text size, your browser remembers that choice on your own device so pages stay easy to read. You can clear it at any time in your browser settings.</p>
    <h2>Protecting your information</h2>
    <p>We use appropriate practices to protect the information you share with us against unauthorized access, alteration, disclosure or destruction. Please don’t send medical records through email; we’ll discuss health details with you by phone.</p>
    <h2>Other websites</h2>
    <p>Our pages link to other websites, such as Onslow County programs, Google Maps and helpful articles. We don’t control those sites and aren’t responsible for their content or privacy practices.</p>
    <h2>Changes to this policy</h2>
    <p>We may update this policy from time to time. When we do, we’ll change the date at the top of this page.</p>
    <h2>Contact us</h2>
    <p>Rapture Ready Home Care<br>{B['street']}<br>{B['city']}<br><a href="tel:{B['tel']}">{B['phone']}</a><br><a href="mailto:{B['email']}">{B['email']}</a></p>
  </div>
</section>'''
    return pg, shell(pg, 'Privacy Policy | Rapture Ready Home Care', 'How the Rapture Ready Home Care website handles your information.', body)


def not_found():
    pg = Page('')
    body = f'''<section class="phead"><div class="wrap phead__in"><div class="phead__txt">
<h1>We couldn’t find that page</h1><p class="lead">The page may have moved when our website was updated. Try one of these instead, or call us at <a href="tel:{B['tel']}">{B['phone']}</a>.</p>
<p class="hero__actions"><a class="btn btn--primary" href="/">Go to the home page</a> <a class="btn btn--outline" href="/our-services/">See our services</a></p></div></div></section>'''
    html_ = shell(pg, 'Page not found | Rapture Ready Home Care', 'Page not found.', body)
    # 404 is served from any path, so use absolute links
    html_ = html_.replace('href="./', 'href="/').replace('src="assets/', 'src="/assets/').replace('href="assets/', 'href="/assets/')
    html_ = re.sub(r'href="(about-us|our-services|hope-at-home|contact-us|request-care|privacy-policy)/"', r'href="/\1/"', html_)
    return html_


# ---------------------------------------------------------------------------
def write(pg, text):
    d = os.path.join(ROOT, pg.slug) if pg.slug else ROOT
    os.makedirs(d, exist_ok=True)
    with open(os.path.join(d, 'index.html'), 'w') as f:
        f.write(text)
    return pg.slug


def main():
    data = json.load(open(os.path.join(ROOT, '_src', 'articles.json')))
    slugs = []
    for fn in (home, about, services, request_care, contact, hope, privacy):
        slugs.append(write(*fn()))
    for key in CATS:
        slugs.append(write(*category(key)))
    slugs.append(write(*alias('get-active', 'nurses-corner', 'Nurse’s Corner')))
    slugs.append(write(*alias('nutrition-blog', 'nurses-corner', 'Nurse’s Corner')))
    for meta in ARTICLES:
        slugs.append(write(*article(meta, data[meta[0]])))
    with open(os.path.join(ROOT, '404.html'), 'w') as f:
        f.write(not_found())
    today = date.today().isoformat()
    urls = ''.join(f'<url><loc>{DOMAIN}/{s + "/" if s else ""}</loc><lastmod>{today}</lastmod></url>'
                   for s in slugs if s not in ('get-active', 'nutrition-blog'))
    open(os.path.join(ROOT, 'sitemap.xml'), 'w').write(f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">{urls}</urlset>\n')
    open(os.path.join(ROOT, 'robots.txt'), 'w').write(f'User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n')
    print(f'built {len(slugs)} pages')


if __name__ == '__main__':
    main()
