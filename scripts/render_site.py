#!/usr/bin/env python3
"""Render the static portfolio from this file. Run from the repo root."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
EMAIL = "jasminejwilson1@gmail.com"
RESUME = "https://drive.google.com/file/d/1FDNk9_3ZM3FPRy4modiEh6E8gpLfwyuB/view?usp=sharing"
LINKEDIN = "https://www.linkedin.com/in/jasminejwilson/"
GITHUB = "https://github.com/HeyJasmineJ/UX-Portfolio"
TITLE = "Senior UX Engineer"
META = "Jasmine Wilson is a senior UX engineer in Austin, TX."


def asset(depth: int, path: str) -> str:
    return ("../" * depth) + path


def page(depth: int, title: str, path: str, body: str, current: str) -> str:
    css = asset(depth, "css/site.css")
    js = asset(depth, "js/site.js")
    fav = asset(depth, "media/favicon.png")
    home = asset(depth, "index.html") if depth else "./"
    about = asset(depth, "about/")
    work = asset(depth, "project/")
    skills = f"{home}#skills"
    contact = f"{home}#contact"
    if path.rstrip("/") in {".", ""}:
        home_cur = ' aria-current="page"'
    else:
        home_cur = ""
    about_cur = ' aria-current="page"' if current == "about" else ""
    work_cur = ' aria-current="page"' if current == "work" else ""
    return f"""<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{title}</title>
  <meta name="description" content="{META}">
  <meta property="og:title" content="{title}">
  <meta property="og:description" content="{META}">
  <link rel="icon" href="{fav}">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:ital,wght@0,400;0,700;1,400&family=Newsreader:ital,opsz,wght@0,6..72,400;0,6..72,600;1,6..72,400&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="{css}">
</head>
<body>
  <a class="skip" href="#main">Skip to content</a>
  <header class="site-header wrap">
    <a class="site-name" href="{home}">Jasmine Wilson</a>
    <button class="nav-toggle" type="button" aria-expanded="false">Menu</button>
    <nav class="site-nav" aria-label="Primary">
      <a href="{home}"{home_cur}>Home</a>
      <a href="{work}"{work_cur}>Work</a>
      <a href="{about}"{about_cur}>About</a>
      <a href="{skills}">Skills</a>
      <a href="{contact}">Contact</a>
    </nav>
    <a class="resume" href="{RESUME}">Resume</a>
  </header>
  <main id="main">
{body}
  </main>
  <footer class="site-footer wrap">
    <p><a href="mailto:{EMAIL}">{EMAIL}</a> · <a href="{LINKEDIN}">LinkedIn</a> · Austin, TX</p>
    <p>This site is HTML, CSS, and a little JavaScript. <a href="{GITHUB}">Source on GitHub</a>.</p>
  </footer>
  <script src="{js}"></script>
</body>
</html>
"""


WORK = [
    {
        "slug": "claritea",
        "name": "Claritea",
        "role": "Design and front-end",
        "lede": "I interviewed ADHD and wellness readers, then designed and built a session-based reading app — Focus Score from heart rate, not a yearly streak.",
        "thumb": "media/claritea.jpg",
        "alt": "Claritea reading app on a desktop",
    },
    {
        "slug": "nevro",
        "name": "Nevro",
        "role": "Design and front-end",
        "lede": "I sat with physicians in clinic, then designed the HCP Portal, patient app, and design system so they could monitor implants themselves.",
        "thumb": "media/nevro.png",
        "alt": "Nevro patient monitoring screens",
    },
    {
        "slug": "arrive-logistics",
        "name": "Arrive Logistics",
        "role": "UX/UI design",
        "lede": "I shadowed carriers on live calls. What they did and what they said didn’t match — the new board followed the workarounds.",
        "thumb": "media/arrive.png",
        "alt": "Arrive Logistics load board",
    },
    {
        "slug": "qualtrics",
        "name": "Qualtrics",
        "role": "UX/UI design",
        "lede": "I designed mobile almost from scratch — Magic Link with security, dashboards rebuilt for touch — and redesigned Create UI after testing how people actually start a survey.",
        "thumb": "media/qualtrics.png",
        "alt": "Qualtrics survey product",
    },
    {
        "slug": "punchh",
        "name": "Punchh",
        "role": "UX/UI design",
        "lede": "Sole mobile designer. Competitive audit, then a white-label system that could do points or punch cards, simple add-ons or a full builder.",
        "thumb": "media/punchh.png",
        "alt": "Punchh restaurant app",
    },
    {
        "slug": "vodii-flueid",
        "name": "Vodii (Flueid)",
        "role": "Design, front-end and PM",
        "lede": "I audited what we could keep, rebuilt the rest, and wrote the production front-end. Signing, sharing, tracking first — then a system that could take new features.",
        "thumb": "media/vodii.png",
        "alt": "Vodii document platform",
    },
    {
        "slug": "tripping",
        "name": "Tripping",
        "role": "UX design",
        "lede": "First UX role. I audited homepage through listings, then worked with engineering to rank host photos with ML so the first image wasn’t a dark kitchen.",
        "thumb": "media/tripping.png",
        "alt": "Tripping vacation rentals",
    },
]


def work_list(depth: int) -> str:
    items = []
    for item in WORK:
        href = asset(depth, f"project/{item['slug']}/")
        src = asset(depth, item["thumb"])
        items.append(
            f"""    <a class="work-item" href="{href}">
      <img src="{src}" alt="{item['alt']}" width="1280" height="720">
      <h3>{item['name']}</h3>
      <p class="role">{item['role']}</p>
      <p>{item['lede']}</p>
    </a>"""
        )
    return "\n".join(items)


def gallery(depth: int, slug: str, count: int, ext: str = ".png") -> str:
    tags = []
    for i in range(1, count + 1):
        src = asset(depth, f"media/{slug}-{i:02d}{ext}")
        tags.append(f'      <img src="{src}" alt="">')
    return "    <div class=\"gallery\">\n" + "\n".join(tags) + "\n    </div>"


def mixed_gallery(depth: int, files: list[str], alt: str) -> str:
    tags = []
    for name in files:
        src = asset(depth, f"media/{name}")
        tags.append(f'      <img src="{src}" alt="{alt}">')
    return "    <div class=\"gallery\">\n" + "\n".join(tags) + "\n    </div>"


CASES = {
    "claritea": {
        "client": "Personal product",
        "intro": "Claritea treats reading as nervous-system care, not a catalog or a streak contest. I designed and built it: sessions tied to heart rate (HealthKit / Health Connect), turned into a Focus Score — how the reading landed in the body, not how many books you owed the year.",
        "sections": [
            (
                "The problem",
                [
                    "Most reading apps still optimize for shelves, ratings, and yearly challenges. Wellness apps track meditation and sleep—but leave reading out. For ADHD readers especially, volume-based gamification often makes the guilt worse.",
                    "I interviewed aspirational readers, ADHD readers, and people who already use Calm-style tools. Proof motivated more than advice. Seeing a calm signal after a session made the value feel real.",
                    "I mapped the competitors: Bookly and Basmo count minutes; Fable and Goodreads do community; wellness apps ignore books. Nothing sat at session tracking + biometric wellness + ADHD-first UX.",
                ],
            ),
            (
                "What I made",
                [
                    "Design principles I used as a filter: reading as self-care, not homework; ADHD-first as universal design; show the body’s response instead of lecturing; intimate social over broadcast.",
                    "I prototyped the core loop in HTML, then implemented production front-end in React Native (Expo) with a shared Supabase backend and a SwiftUI Mac companion. This isn’t only screens.",
                    "The loop is simple: open a book → start a Focus Session → optional ADHD check-ins → end session → Focus Score. Founder-built and production-ready — not an App Store launch with invented engagement numbers.",
                ],
            ),
        ],
        "images": [f"claritea-{i:02d}.png" for i in range(1, 14)],
    },
    "nevro": {
        "client": "Nevro Corp",
        "intro": "I was Nevro’s first in-house designer. Physicians couldn’t monitor implant patients unless the company sent an update — competitors already had remote monitoring. I did the research in clinic, then designed the HCP Portal, the patient app, and the design system. Front-end and the regulatory docs were part of the job.",
        "sections": [
            (
                "Research and process",
                [
                    "I was the only designer. I ran usability studies and sat with physicians while they used the Programmer and the existing app in clinic. They needed the last session, a trend over time, and a way to jump to the patient who needed a call — during the visit, not after.",
                    "The HCP Portal, patient app, and Programmer had been designed as separate products. I mapped how data had to move between them. Healthcare regs, security, and wireless talk to an implant all shaped what we could actually ship.",
                ],
            ),
            (
                "What shipped",
                [
                    "The HCP Portal was the centerpiece — a web dashboard for one patient or a whole panel. I designed visualizations to spot who needed attention, kept urgent data up front, and put history one click in.",
                    "The patient app got a real connection to the implant so people could log pain in the moment and their physician could see it without a separate upload. That work had to hold up for people in chronic pain: readable type, contrast that survived clinic lighting, and targets you could hit on a bad day. Accessibility wasn’t a separate pass; it was part of designing for patients.",
                    "I designed and coded a design system for mobile, desktop, and email, then handed the base components to engineering so the three surfaces didn’t drift.",
                    "The MVP launched in the US. Physicians could finally look at patient data themselves. That’s table stakes in this market; Nevro just didn’t have it yet.",
                ],
            ),
        ],
        "images": [
            "nevro-01.png",
            "nevro-02.png",
            "nevro-03.jpg",
            "nevro-04.png",
            "nevro-05.png",
            "nevro-06.jpg",
            "nevro-07.png",
            "nevro-08.webp",
            "nevro-09.webp",
            "nevro-10.webp",
        ],
    },
    "arrive-logistics": {
        "client": "Arrive Logistics",
        "intro": "Arrive’s load board was Excel with a login. Carriers hunted for shipping details while a customer was on the line. I shadowed them, tested on their desks, and designed for desktop — that’s where the work happens.",
        "sections": [
            (
                "Research and process",
                [
                    "I started with interviews and dozens of wires. A carrier’s day touches more systems than you’d think, and they’re switching context the whole time.",
                    "The useful part was sitting next to them on live calls. They’d say a feature mattered and then never touch it — they’d use a workaround instead. That became the design brief.",
                    "It’s a desktop job, so I skipped mobile-first. Each version went back to carriers at their desks the same week. We threw away a few complete layouts.",
                ],
            ),
            (
                "What shipped",
                [
                    "I stopped treating it like a grid of cells. The fields they actually used on calls sat up top. Everything else was still there, just quieter.",
                    "Related fields lived together so they weren’t hopping tabs for one decision. Contrast, spacing, and type made zones — not more grid lines.",
                    "They could find a load faster, especially when the board was slammed. Less time fighting the tool, more time on the call.",
                ],
            ),
        ],
        "images": [f"arrive-{i:02d}.png" for i in range(1, 8)],
    },
    "qualtrics": {
        "client": "Qualtrics",
        "intro": "I joined Qualtrics during a growth stretch. The mobile app became mine, basically from scratch — including Magic Link, which had to satisfy security after the acquisition — and Create UI, the screen that starts every survey.",
        "sections": [
            (
                "Research and process",
                [
                    "Qualtrics is a dense desktop tool. We needed a mobile app that didn’t feel like a shrunk dashboard, plus a sign-in flow that would pass post-acquisition security.",
                    "I didn’t scale the desktop down. I picked what people actually open on a phone and rebuilt the rest for touch. Engineering was in Krakow. I was in Sketch, then Figma.",
                    "Create UI was a different job. I inherited the first screen of survey building — scratch or template — and it showed. I built high-fidelity prototypes, tested them, and wrote up the patterns so they could feed the roadmap.",
                ],
            ),
            (
                "What shipped",
                [
                    "Magic Link let people in without a password on their phone, and security signed off.",
                    "Mobile dashboards lead with the frequent stuff. The rest is one tap further. Targets are actually tappable.",
                    "Create UI got a clearer template picker and a less confusing path if you start from zero. Engineering built close to the prototypes. The mobile work is in the production app.",
                ],
            ),
        ],
        "images": [
            "qualtrics-01.png",
            "qualtrics-02.png",
            "qualtrics-03.png",
            "qualtrics-04.gif",
            "qualtrics-05.png",
            "qualtrics-06.gif",
            "qualtrics-07.png",
            "qualtrics-08.gif",
            "qualtrics-09.gif",
        ],
    },
    "punchh": {
        "client": "Punchh",
        "intro": "I was the only mobile designer at Punchh and owned the white-label framework behind hundreds of restaurant apps. Delivery took off during COVID and our UI looked old.",
        "sections": [
            (
                "Research and process",
                [
                    "White-label is the whole problem. A QSR and a sit-down place don’t want the same app. Some care about points, some about modifiers. One system had to cover that without looking generic.",
                    "I started with a competitive audit of the restaurant apps people already used — not to copy them, to see which patterns had become expected. Then I wired deals, customize, rewards.",
                    "A lot of UI versions. Stakeholders picked apart each one. The question was always: can another brand skin this without breaking checkout, rewards, or the order flow?",
                ],
            ),
            (
                "What shipped",
                [
                    "Navigation, hierarchy, and buttons stayed consistent. Color, logo, photos, and menu shape could move.",
                    "Rewards could be points, punch cards, or tiers. Food customization could be “add bacon” or a full builder. Same frame.",
                    "Restaurants using Punchh could look current without giving up how they look. For Punchh it was the difference between “fine” and “we can keep this account.”",
                ],
            ),
        ],
        "images": [f"punchh-{i:02d}.png" for i in range(1, 8)],
    },
    "vodii-flueid": {
        "client": "Vodii / Flueid",
        "intro": "At Vodii I was the designer, the front-end, and the project manager. TxM handled real estate documents on a stack that couldn’t take new work. I audited what we could keep, rebuilt the rest, and implemented the production front-end.",
        "sections": [
            (
                "Research and process",
                [
                    "I was the only designer (two of us after Flueid bought Vodii). I also ran the timeline and made technical calls. That’s the job when the team is that small.",
                    "First pass was an audit: what could we keep inside the old framework, and what had to be rebuilt. Then a modular architecture — reusable components so the next feature didn’t mean another rewrite.",
                    "Working alone is fast until you pick the wrong thing. I kept the first release to signing, sharing, and tracking, and left room in the system for what came next.",
                ],
            ),
            (
                "What shipped",
                [
                    "New UI, yes — but the useful part was the structure. Common document tasks took fewer steps.",
                    "Because I was writing the production front-end, the file and the browser didn’t drift apart. Later people could touch one feature without untangling the whole thing.",
                    "After Flueid acquired Vodii, this was still the base.",
                ],
            ),
        ],
        "images": [f"vodii-{i:02d}.png" for i in range(1, 13)],
    },
    "tripping": {
        "client": "Tripping",
        "intro": "This was my first UX role. Tripping had never had a dedicated UX designer. I started with an audit of homepage, search, and listings, then worked with engineering on ML photo ranking so the first image wasn’t a dark kitchen.",
        "sections": [
            (
                "Research and process",
                [
                    "Search is the product: people compare a pile of rentals and drown in amenities, prices, location, and availability. I had to make that scannable without hiding the details they need to book.",
                    "More people browsed on phones; bookings still happened on desktop. Both had to work.",
                    "Research surfaced a problem that wasn’t in the original brief: photos. Hosts upload whatever — dark, blurry, one good picture buried at the end. I worked with engineering on a machine-learning ranker so the first photo wasn’t arbitrary.",
                ],
            ),
            (
                "What shipped",
                [
                    "Filters narrow without a wall of options. Price, place, and the one or two amenities that matter sit up front.",
                    "The photo ranking was the part people felt. Same listings, better first impression. Engagement and conversion both moved. I don’t have the exact numbers in front of me anymore, so I’m not going to invent them.",
                    "The brief didn’t mention the photos. That’s usually how it goes.",
                ],
            ),
        ],
        "images": [f"tripping-{i:02d}.png" for i in range(1, 10)],
    },
}


def home() -> str:
    d = 0
    portrait = asset(d, "media/portrait.jpg")
    return f"""    <section class="hero wrap">
      <p class="hero-kicker">{TITLE} · Austin · open to work</p>
      <h1>UX engineer in Austin. I design the interface, and I can write the code.</h1>
      <p class="hero-actions">
        <a href="#contact">Contact</a>
        <a href="{RESUME}">Resume</a>
      </p>
    </section>
    <section class="section wrap" id="work">
      <h2>Work</h2>
      <div class="work-list">
{work_list(d)}
      </div>
    </section>
    <section class="section wrap intro">
      <div>
        <h2>About the work</h2>
        <p>I’m a UX engineer and front-end developer in Austin. Eight years of healthcare, enterprise software, logistics, and consumer apps — usually as the only designer, and often writing the production front-end too.</p>
        <p>I don’t just make pictures of interfaces. I know how they get built, so the work stays realistic. Whether that’s a design system, research in a clinic, or production React, I want the thing to work in someone’s actual day.</p>
        <p><a href="{asset(d, 'about/')}">More about me</a></p>
      </div>
      <img src="{portrait}" alt="Portrait of Jasmine Wilson" width="800" height="1000">
    </section>
    <section class="section wrap" id="skills">
      <h2>Skills</h2>
      <div class="skills">
        <div>
          <h3>Product design</h3>
          <p>Research, wires, prototypes, and UI — usually in that order. Web and mobile, with accessibility in the same pass as the screens.</p>
        </div>
        <div>
          <h3>Design systems</h3>
          <p>Component libraries that survive contact with engineering. I built these from scratch at Nevro, Vodii, and Punchh.</p>
        </div>
        <div>
          <h3>Accessibility</h3>
          <p>Readable type, contrast, and targets that still work when someone is in pain, in a hurry, or on a small phone. I designed for that on Nevro’s patient app and I look for it everywhere else.</p>
        </div>
        <div>
          <h3>Production front-end</h3>
          <p>React, HTML, CSS, and JavaScript that shipped — not throwaway prototypes. I wrote the front-end at Vodii, coded the Nevro design system, and built Claritea in React Native.</p>
        </div>
      </div>
    </section>
    <section class="section wrap">
      <h2>A few practical things</h2>
      <dl class="faq">
        <dt>What kind of work do you take on?</dt>
        <dd>Product design for web and mobile — healthcare, enterprise, consumer. Redesigns, design systems, apps I’ll also help build. I’m less useful on a brand-only project.</dd>
        <dt>Do you code as well as design?</dt>
        <dd>Yes. Production front-end in React, HTML, CSS, and JavaScript. I can go from a wireframe to something that ships.</dd>
        <dt>What’s your design process?</dt>
        <dd>Talk to the people who use it, make the problem specific, then wires and prototypes. I test when I can. If I’m also building, I write the components.</dd>
        <dt>What’s your availability?</dt>
        <dd>I’m looking for the next role, and I’ll take on the right project.</dd>
        <dt>Do you work remotely?</dt>
        <dd>Yes. I’m in Austin and used to working with teams in other time zones — Qualtrics engineering was in Krakow.</dd>
        <dt>Contract or full-time?</dt>
        <dd>Both. We can figure out the shape on a call.</dd>
      </dl>
    </section>
    <section class="section wrap contact" id="contact">
      <div>
        <h2>Get in touch</h2>
        <p>Want to talk? Say hi.</p>
        <dl class="meta-list">
          <div><dt>Based in</dt><dd>Austin, TX</dd></div>
          <div><dt>Email</dt><dd><a href="mailto:{EMAIL}">{EMAIL}</a></dd></div>
        </dl>
      </div>
      <form data-contact>
        <label>Name <input name="name" required></label>
        <label>Email <input name="email" type="email" required></label>
        <label>Message <textarea name="message" required></textarea></label>
        <button type="submit">Send</button>
      </form>
    </section>
"""


def about_page() -> str:
    d = 1
    film = [
        ("travel-1.png", "Travel photograph by Jasmine Wilson"),
        ("travel-2.png", "Travel photograph by Jasmine Wilson"),
        ("travel-3.png", "Travel photograph by Jasmine Wilson"),
        ("travel-4.png", "Travel photograph by Jasmine Wilson"),
    ]
    film_html = "\n".join(
        f'      <img src="{asset(d, "media/" + n)}" alt="{alt}">' for n, alt in film
    )
    return f"""    <section class="hero wrap">
      <p class="hero-kicker">About</p>
      <h1>I’m in Austin. When I’m not designing, I’m usually traveling or taking pictures.</h1>
    </section>
    <div class="film wrap">
{film_html}
    </div>
    <section class="section wrap intro">
      <div>
        <p>Eight years in design since 2017 — healthcare, logistics, fintech, and enterprise software. Six major product launches. I design the experience and I can build the front-end.</p>
        <p>I founded Colorful Coders (youth tech education) and The Kinnect (design agency).</p>
        <p>When I’m not designing, I’m teaching kids to code through <a href="https://www.colorfulcoders.com/">Colorful Coders</a> or running my design agency, <a href="https://www.thekinnect.com/">The Kinnect</a>.</p>
      </div>
      <img src="{asset(d, "media/jasmine.jpg")}" alt="Jasmine Wilson" width="900" height="700">
    </section>
    <section class="section wrap" id="skills">
      <h2>What I do</h2>
      <div class="skills">
        <div>
          <h3>Design systems</h3>
          <p>I’ve built design systems from scratch at Nevro, Vodii, and Punchh — component libraries that scale across mobile, web, and email.</p>
        </div>
        <div>
          <h3>Mobile-first thinking</h3>
          <p>Restaurant apps, patient tools, enterprise surveys — the hard part is making the dense stuff work on a phone.</p>
        </div>
        <div>
          <h3>User research</h3>
          <p>I’ve shadowed carriers during calls, observed physicians in clinical settings, and run usability studies — because the screens have to match the actual day.</p>
        </div>
        <div>
          <h3>Accessibility</h3>
          <p>Especially on healthcare work. The Nevro patient app had to stay usable for people logging pain, not just for a demo on a good screen.</p>
        </div>
        <div>
          <h3>Production front-end</h3>
          <p>I implement my own designs in production code and sit with engineering without a translation layer.</p>
        </div>
      </div>
    </section>
"""


def listing() -> str:
    d = 1
    return f"""    <section class="hero wrap">
      <p class="hero-kicker">Work</p>
      <h1>These are the projects I can talk about in some detail. Healthcare, enterprise, and a product I built myself.</h1>
    </section>
    <section class="section wrap">
      <p>I’m a UX engineer and front-end developer in Austin. I studied art and computer science. I design the interface and I often write the code, which keeps me honest about what’s actually possible.</p>
      <p>I’ve spent the last eight years as the lead — and often only — designer at places like Nevro, Qualtrics, and Punchh. Understand the actual problem, then make the simplest thing that works.</p>
      <p>When I’m not designing, I’m teaching kids to code through <a href="https://www.colorfulcoders.com/">Colorful Coders</a> or running my design agency, <a href="https://www.thekinnect.com/">The Kinnect</a>.</p>
    </section>
    <section class="section wrap">
      <div class="work-list">
{work_list(d)}
      </div>
    </section>
"""


def case_page(slug: str, item: dict) -> str:
    d = 2
    data = CASES[slug]
    back = asset(d, "project/")
    hero = asset(d, item["thumb"])
    blocks = []
    for heading, paras in data["sections"]:
        blocks.append(f"      <h2>{heading}</h2>")
        for para in paras:
            blocks.append(f"      <p>{para}</p>")
    gallery = mixed_gallery(d, data["images"], item["name"])
    return f"""    <article class="wrap case-hero">
      <a class="back" href="{back}">All work</a>
      <h1>{item['name']}</h1>
      <p class="case-meta">{item['role']} · {data['client']}</p>
      <p class="lead">{data['intro']}</p>
      <img src="{hero}" alt="{item['alt']}" width="1280" height="720">
    </article>
    <section class="section wrap prose">
{chr(10).join(blocks)}
    </section>
{gallery}
"""


def not_found() -> str:
    return """    <section class="hero wrap">
      <h1>That page isn’t here.</h1>
      <p><a href="./">Back home</a></p>
    </section>
"""


def write(rel: str, html: str) -> None:
    path = ROOT / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(html, encoding="utf-8")
    print("wrote", rel, "bytes", path.stat().st_size)


def main() -> None:
    write(
        "index.html",
        page(0, f"Jasmine Wilson — {TITLE}", "/", home(), "home"),
    )
    write(
        "about/index.html",
        page(1, f"About — Jasmine Wilson", "/about", about_page(), "about"),
    )
    write(
        "project/index.html",
        page(1, f"Work — Jasmine Wilson", "/project", listing(), "work"),
    )
    for item in WORK:
        write(
            f"project/{item['slug']}/index.html",
            page(
                2,
                f"{item['name']} — Jasmine Wilson",
                f"/project/{item['slug']}",
                case_page(item["slug"], item),
                "work",
            ),
        )
    write("404.html", page(0, f"Not found — Jasmine Wilson", "/404", not_found(), ""))


if __name__ == "__main__":
    main()
