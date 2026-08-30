#!/usr/bin/env python3
"""Replace leftover template copy with Jasmine's voice."""

from __future__ import annotations

import html as html_lib
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LETTER_STYLE = (
    "display:inline-block;opacity:0.001;transform:translateX(0px) "
    "translateY(50px) scale(1) rotate(0deg) skewX(0deg) skewY(0deg)"
)
WORD_GROUP = (
    r'<span style="white-space:(?:nowrap|unset)">'
    r'(?:<span style="display:inline-block;opacity:0\.001;[^"]+">[^<]*</span>)*'
    r"</span>"
)
REGION = re.compile(rf"(?:{WORD_GROUP}\s*)+")


def decode_region(region: str) -> str:
    parts = re.split(r'</span>\s*<span style="white-space:(?:nowrap|unset)">', region)
    words = []
    for part in parts:
        letters = re.findall(r'<span style="display:inline-block[^"]*">([^<]*)</span>', part)
        words.append(html_lib.unescape("".join(letters)))
    return " ".join(w for w in words if w)


def encode_split(text: str) -> str:
    def word_html(word: str) -> str:
        letters = "".join(
            f'<span style="{LETTER_STYLE}">{html_lib.escape(ch)}</span>' for ch in word
        )
        return f'<span style="white-space:nowrap">{letters}</span>'

    return " ".join(word_html(word) for word in text.split(" "))


def replace_split(html: str, old: str, new: str) -> str:
    def repl(match: re.Match[str]) -> str:
        decoded = decode_region(match.group(0))
        if decoded == old:
            return encode_split(new)
        return match.group(0)

    return REGION.sub(repl, html)


def replace_all(html: str, pairs: list[tuple[str, str]]) -> str:
    for old, new in pairs:
        if old not in html:
            continue
        html = html.replace(old, new)
    return html


def set_image_alt(html: str, filename: str, alt: str) -> str:
    def repl(match: re.Match[str]) -> str:
        tag = match.group(0)
        if filename not in tag:
            return tag
        if "alt=" in tag:
            return re.sub(r'alt="[^"]*"', f'alt="{alt}"', tag)
        return tag[:-1] + f' alt="{alt}">'

    return re.sub(r"<img\b[^>]*>", repl, html)


GLOBAL_PAIRS = [
    (" - Modio Template", " — Jasmine Wilson"),
    (
        "Jasmine Wilson a Senior UX Design Engineer based in Austin, TX",
        "Jasmine Wilson is a senior UX design engineer in Austin, TX.",
    ),
    ("The Challenge &amp; Process", "The problem"),
    ("The Solution &amp; Impact", "What I made"),
    ("What I Do Best.", "What I do"),
    ("Your questions, answered.", "A few practical things."),
    (
        "Thinking about working together? Here are answers to questions I hear most often.",
        "What people usually ask before we get on a call.",
    ),
    ("Let’s build together.", "Get in touch."),
    ("Have a project in mind?", "Want to talk?"),
    ("Let's Chat", "Say hi"),
    ("Open to New Opportunities", "Open to work"),
    ("A Curated Selection", "Selected work"),
    (
        "Design that lasts. Brands that resonate. Experiences that inspire.",
        "Research in the room. Design that ships. Photos from the road.",
    ),
    (">Services<", ">Skills<"),
    ("Yellow Bottle on Yellow Background", "Arrive Logistics load board"),
    ("Stylish Modern Wristwatch", "Qualtrics survey product"),
    ("Person with VR Headset", "Punchh restaurant app"),
    ("Futuristic Humanoid Robot", "Tripping vacation rentals"),
    ("Office Discussion", "Jasmine Wilson"),
    ("Contemplative Profile Against Colorful Backdrop", "Portrait of Jasmine Wilson"),
    ("Minimalist Tropical Decor", "Still life photographed by Jasmine Wilson"),
    ("Colorful Coats in Motion", "Colorful coats, photographed by Jasmine Wilson"),
    ("Elegant Hydration_ Citrus and Sky", "Citrus drink against a blue sky"),
    ("Minimalist Composition with Spheres", "Still life with spheres"),
    ("Person Walking Against Two-Toned Wall", "Person walking past a two-tone wall"),
    ("Potted Plant Against Vivid Yellow Backdrop", "Plant against a yellow wall"),
    ("Years in Design", "Years in UX"),
]

FAQ_PAIRS = [
    (
        "What kind of projects do you take on?",
        "What kind of work do you take on?",
    ),
    (
        "I specialize in UX/UI design for web and mobile products, with particular expertise in healthcare, enterprise software, and consumer apps. I work on everything from complete product redesigns to design system creation to mobile app development",
        "Product design for web and mobile — healthcare, enterprise, consumer. Redesigns, design systems, apps I’ll also help build. I’m less useful on a brand-only project.",
    ),
    (
        "Yes. I'm a full-stack designer with front-end development skills in React, HTML, CSS, and JavaScript. I can take projects from wireframe to production-ready code.",
        "Yes. React, HTML, CSS, JavaScript. I can go from a wireframe to something that runs.",
    ),
    (
        "I start with user research and problem definition, move through wireframing and prototyping with iterative testing, and deliver high-fidelity designs with documentation. For projects where I'm also developing, I build production-ready components.",
        "Talk to the people who use it, make the problem specific, then wires and prototypes. I test when I can. If I’m also building, I write the components.",
    ),
    (
        "I am currently open to new opportunities and accepting projects.",
        "I’m looking for the next role, and I’ll take on the right project.",
    ),
    (
        "Yes, I'm available for remote work and have extensive experience collaborating with distributed teams across time zones.",
        "Yes. I’m in Austin and used to working with teams in other time zones — Qualtrics engineering was in Krakow.",
    ),
    (
        "Yes, I'm open to both contract engagements and consulting arrangements. Let's discuss what works best for your needs.",
        "Both. We can figure out the shape on a call.",
    ),
    (
        "Do you offer consulting or contract work?",
        "Contract or full-time?",
    ),
]

SKILL_PAIRS = [
    (
        "User research, wireframing, prototyping, and visual design for web and mobile products. I create intuitive interfaces that prioritize user needs while meeting business goals.",
        "Research, wires, prototypes, and UI — usually in that order. Web and mobile.",
    ),
    (
        "Building scalable component libraries and design systems that maintain consistency across platforms. From documentation to implementation, I create systems that empower teams.",
        "Component libraries that survive contact with engineering. I built these from scratch at Nevro, Vodii, and Punchh.",
    ),
    (
        "Specializing in mobile-first experiences and responsive design. I've designed mobile apps for healthcare, enterprise surveys, and white-label restaurant frameworks serving millions of users.",
        "Patient apps, enterprise survey tools, restaurant apps used by a lot of brands. Small screens, real constraints.",
    ),
    (
        "Bringing designs to life with clean, maintainable code. I prototype in React, build production-ready components, and collaborate effectively with engineering teams.",
        "I prototype in React and I can hand over something engineers don’t have to rebuild.",
    ),
    (
        "From white-label restaurant apps to healthcare patient tools, I specialize in making complex functionality work seamlessly on small screens.",
        "Restaurant apps, patient tools, enterprise surveys — the hard part is making the dense stuff work on a phone.",
    ),
    (
        "My front-end development background means I can prototype in code, implement my own designs, and collaborate effectively with engineering teams.",
        "I can prototype in code, implement my own designs, and sit with engineering without a translation layer.",
    ),
    (
        "Crafting user experiences across healthcare, logistics, fintech, and enterprise software.",
        "Healthcare, logistics, fintech, and enterprise software.",
    ),
    (
        "From mobile frameworks to healthcare portals, each solving real user problems.",
        "Mobile frameworks, healthcare portals, and a couple of companies I started.",
    ),
    (
        "Full-stack designer who both designs the experience and builds the front-end.",
        "I design the experience and I can build the front-end.",
    ),
]

CARD_PAIRS = [
    (
        "Claritea is a reading wellness app that treats reading as nervous-system care—not a catalog or streak contest.",
        "A reading app I designed and built. Sessions, not streaks — and a Focus Score from heart rate, not guilt.",
    ),
    (
        "Designing an integrated healthcare ecosystem that empowers physicians to remotely monitor pain management patients, bridging the gap between mobile patient apps and clinical oversight tools.",
        "Remote monitoring for pain patients. Physicians could finally see implant data without waiting on the company.",
    ),
    (
        "Physicians gained autonomous access to patient data without company intermediaries, enabling consistent patient support and faster response to treatment needs. The MVP launched successfully in the US market, establishing Nevro's competitive parity in remote patient monitoring.",
        "First in-house designer. Portal, patient app, and a design system. The MVP shipped in the US.",
    ),
    (
        "Transforming an Excel-like interface into a modern, scannable load board that helps carriers process shipping information faster during high-pressure customer calls.",
        "The load board used to look like Excel. I sat with carriers on live calls and redesigned it so they could find a load mid-sentence.",
    ),
    (
        "Carriers could process load information significantly faster, improving operational efficiency during peak times. The modern interface reduced cognitive load and supported better decision-making during time-sensitive customer interactions.",
        "Desktop-first. A few full rewrites. Faster to scan when the board is slammed.",
    ),
    (
        "Transforming complex desktop survey tools into an intuitive mobile experience while redesigning the critical Create UI interface used by thousands of enterprise customers.",
        "Mobile app, Magic Link sign-in, and the Create UI that starts every survey. The mobile work is in the live product.",
    ),
    (
        "My mobile designs are now live in the production app, providing Qualtrics users with on-the-go access to essential features. The Create UI redesign improved the critical first interaction users have with the platform, with high-fidelity prototypes closely matching the eventual live implementation.",
        "Worked with engineering in Krakow. Prototypes that actually matched what shipped.",
    ),
    (
        "Modernizing a white-label restaurant app framework used by hundreds of brands nationwide, bringing it to competitive parity during the pandemic surge in mobile delivery orders.",
        "White-label restaurant apps for hundreds of brands. I rebuilt the mobile framework when delivery exploded during COVID.",
    ),
    (
        "The redesigned framework positioned Punchh competitively during a critical growth period when mobile delivery usage surged. Restaurants could offer their customers an experience on par with industry leaders while maintaining their unique brand identity.",
        "One framework, a lot of brand skins. Sole mobile designer.",
    ),
    (
        "Leading a complete platform redesign for real estate document management, modernizing outdated infrastructure to support future growth in an evolving digital landscape.",
        "Real estate document tool on aging tech. I redesigned TxM and wrote the front-end — it stuck around after Flueid bought the company.",
    ),
    (
        "The modernized TxM platform positioned Vodii for sustainable growth with technology infrastructure capable of supporting future feature expansion. Post-acquisition by Flueid, the redesigned system became the foundation for the company's continued development.",
        "Solo designer. Signing, sharing, tracking — then a system that could take new features.",
    ),
    (
        "Leading my first UX role, I redesigned Tripping's entire vacation rental platform from homepage to listings, implementing ML-powered image ranking that improved engagement and conversion rates.",
        "First UX job. I redesigned the vacation rental site, then ranked listing photos with ML because the uploads were a mess.",
    ),
    (
        "The redesign improved user engagement and conversion rates, with the ML-powered image ranking particularly effective at showcasing properties in their best light. The modern interface positioned Tripping competitively in the vacation rental marketplace.",
        "Engagement and conversion went up. The photo ranking did more than the new type.",
    ),
]

SPLIT_BY_FILE = {
    "index.html": [
        (
            "UX Designer & Developer creating user experiences that solve real problems.",
            "UX designer and developer in Austin.",
        ),
        (
            "Experience in numerous fields from healthcare systems to enterprise tools and mobile apps.",
            "I design the interface, and I can write the code.",
        ),
        (
            "I'm a UX designer and front-end developer based in Austin, Texas. With a decade of experience designing and building products for healthcare, enterprise software, logistics, and consumer apps, I bring a unique full-stack perspective to every project.",
            "I'm a UX designer and front-end developer in Austin. Nine years of UX — healthcare, enterprise software, logistics, and consumer apps — usually as the only designer, and often writing the front-end too.",
        ),
        (
            "I don't just design interfaces—I understand how they're built. This means faster iteration, more realistic solutions, and seamless",
            "I don't just make pictures of interfaces. I know how they get built, so the work stays realistic and engineers don't have to translate it.",
        ),
        (
            "collaboration",
            "",
        ),
        (
            "with engineering teams. Whether I'm creating design systems from scratch, conducting user research in clinical settings, or prototyping in code, I focus on one thing: solving real problems for real people.",
            "Whether that's a design system from scratch, research in a clinic, or a prototype in React, I want the thing to work in someone's actual day.",
        ),
        ("Stay Updated", "Notes"),
    ],
    "about/index.html": [
        (
            "I am based in Austin, Texas and when I'm not deisgning I enjoy traveling and photography.",
            "I'm in Austin. When I'm not designing, I'm usually traveling or taking pictures.",
        ),
        ("Stay Updated", "Notes"),
    ],
    "project/index.html": [
        ("Our case studies highlight the process", "These are the projects"),
        (
            "behind each project — from idea to impact.",
            "I can talk about in some detail.",
        ),
        (
            "See how we solve challenges and create design that resonates.",
            "Healthcare, enterprise, and a product I built myself.",
        ),
        (
            "I'm a UX designer and front-end developer based in Austin, Texas. I create user experiences that solve real",
            "I'm a UX designer and front-end developer in Austin. I work on",
        ),
        (
            "healthcare monitoring systems to enterprise software to mobile apps used nationwide.",
            "healthcare tools, enterprise software, and apps people use every day.",
        ),
        (
            "With backgrounds in both art and computer science, I bring a unique perspective to product design. I don't just design interfaces—I often code them too. This means I understand what's possible, what's practical, and how to build design systems that scale.",
            "I studied art and computer science. I design the interface and I often write the code, which keeps me honest about what's actually possible.",
        ),
        (
            "I've spent the last decade as the lead (and often solo) designer at companies like Nevro, Qualtrics, and Punchh, where I've launched products that serve thousands of users daily. My approach is simple: understand the problem deeply, design the simplest solution, and build it well.",
            "I've spent the last nine years as the lead — and often only — designer at places like Nevro, Qualtrics, and Punchh. Understand the actual problem, then make the simplest thing that works.",
        ),
        (
            ". I believe good design should be accessible to everyone.",
            ". I think good design should be available to more people than it is.",
        ),
        ("Stay Updated", "Notes"),
    ],
    "404.html": [
        ("Stay Updated", "Notes"),
    ],
}

# Case study pages also have the footer split heading.
for slug in (
    "claritea",
    "nevro",
    "arrive-logistics",
    "qualtrics",
    "punchh",
    "vodii-flueid",
    "tripping",
):
    SPLIT_BY_FILE[f"project/{slug}/index.html"] = [("Stay Updated", "Notes")]

CASE_PAIRS = {
    "project/claritea/index.html": [
        (
            "Claritea is a reading wellness app that treats reading as nervous-system care—not a catalog or streak contest. I designed and built it as a personal, production-ready product that connects reading sessions to biometric signals (heart rate, HRV via Apple HealthKit / Health Connect) and turns that into a Focus Score: a clear, humane signal of how reading lands in the body. The experience is ADHD-first—check-ins, pacing, and focus tools that support attention without shame—alongside a Mac companion and waitlist-facing marketing.",
            "Claritea treats reading as nervous-system care, not a catalog or a streak contest. I designed and built it: sessions tied to heart rate and HRV (HealthKit / Health Connect), turned into a Focus Score — how the reading landed in the body, not how many books you owed the year. ADHD-first check-ins and pacing, a Mac companion, and a waitlist. Personal project. It runs.",
        ),
        (
            "Competitive work confirmed the white space: trackers (Bookly, Basmo) capture minutes; social apps (Fable, Goodreads) capture community; wellness apps ignore books entirely. Nothing sat at the intersection of",
            "The map was pretty clear: Bookly and Basmo count minutes, Fable and Goodreads do community, wellness apps ignore books. Nobody sat at",
        ),
        (
            "I prototyped the core experience in a high-fidelity interactive HTML prototype (navigation, session flow, spoiler states, Focus Score reveal), then implemented the product in React Native (Expo) with a shared Supabase backend and a native SwiftUI Mac companion—so the case study isn’t only screens, it’s a working system.",
            "I prototyped the core loop in HTML (navigation, session, spoilers, Focus Score), then built it in React Native (Expo) with Supabase and a SwiftUI Mac companion. This isn’t only screens.",
        ),
        (
            "This is a founder-built, production-ready personal project—not a launched App Store product with published MAU or clinical outcomes. What I can stand behind:",
            "Founder-built, production-ready, not an App Store launch with MAU or clinical claims. What I can stand behind:",
        ),
        (
            "A portfolio- and waitlist-ready demo of the core loop (session → Focus Score), with guest/dev gating for honest demos rather than invented engagement metrics.",
            "A waitlist demo of the loop (session → Focus Score), with guest/dev gating so I’m not inventing engagement numbers.",
        ),
    ],
    "project/nevro/index.html": [
        (
            "As Nevro's first and only in-house designer, I led the creation of the HCP Portal—a web-based dashboard that revolutionized how physicians monitor patients with implanted pain relief devices. The challenge was clear: Nevro lacked a crucial feature that competitors offered, forcing physicians to rely on manual company updates. Through extensive user research, including face-to-face sessions with physicians and clinical observations, I designed and built an integrated ecosystem connecting the HCP Portal, mobile patient app, and complete design system. This project required not only UX design but also front-end development and comprehensive healthcare regulatory documentation.",
            "I was Nevro’s first in-house designer. Physicians had no way to monitor implant patients unless the company sent them an update — competitors already had this. I did the research in clinic, then designed the HCP Portal, the patient app connection, and the design system. Front-end and the regulatory docs were part of the job.",
        ),
        (
            "Nevro's pain management system faced a critical gap. Physicians couldn't independently monitor patients with implanted devices—a standard feature among competitors. Instead, they relied on manual company updates, creating delays in care and frustration for healthcare providers. The existing mobile app and Programmer tool operated in isolation, preventing seamless patient monitoring.",
            "Physicians couldn’t see what was happening with their patients’ implants unless Nevro sent them an update. Competitors already had remote monitoring. The patient app and the Programmer tool also didn’t talk to each other.",
        ),
        (
            "Working as the sole designer, I took a research-first approach. I conducted usability studies and spent time face-to-face with physicians, observing how they used devices in clinical settings. These sessions revealed pain points that weren't obvious from a distance—physicians needed quick access to patient data, the ability to monitor trends over time, and tools that fit naturally into their existing workflows.",
            "I was the only designer. I sat with physicians, watched them use the devices in clinic, and ran usability studies. What they needed was pretty plain: patient data without a scavenger hunt, trends over time, and something that fit the visit — not a new workflow.",
        ),
        (
            "I mapped out the entire ecosystem, identifying how the web portal, mobile app, and physician tools needed to communicate. This wasn't just about designing screens—it required understanding healthcare regulations, security requirements, and the technical constraints of wireless connectivity to implanted devices.",
            "Then I mapped the portal, the mobile app, and the physician tools. Healthcare regs, security, and the fact that these things talk wirelessly to an implant all shaped what we could ship.",
        ),
        (
            "I designed and built three interconnected components that transformed patient monitoring at Nevro:",
            "Three pieces:",
        ),
        (
            "The HCP Portal became the centerpiece—a web-based dashboard where physicians could monitor patient data at both individual and population levels. Clean data visualizations made it easy to spot trends and identify patients needing attention. The interface prioritized the most critical information while keeping deeper details accessible when needed.",
            "The HCP Portal was the main one — a web dashboard for one patient or a whole panel. Urgent stuff up front; they could drill in when they needed to.",
        ),
        (
            "For the mobile patient app, I redesigned the experience to seamlessly connect with implanted devices, enabling real-time pain assessment. Patients could track their pain levels and share this data directly with their physicians without additional steps.",
            "The patient app got a real connection to the implant so people could log pain and their physician could see it without extra steps.",
        ),
        (
            "Underpinning everything was a complete design system I created and coded. This included reusable components that maintained consistency across mobile, desktop, and even email communications. I built the base components and shared them with engineers to implement throughout the application.",
            "I also designed and coded a design system — components for mobile, desktop, and email — and handed the base pieces to engineering.",
        ),
        (
            "The impact was immediate. Physicians could now access patient data autonomously, without waiting for company intermediaries. This enabled them to provide consistent support and respond quickly when patients needed treatment adjustments. The MVP successfully launched in the US market, finally bringing Nevro to competitive parity in remote patient monitoring—a capability that had become table stakes in the industry.",
            "The MVP launched in the US. Physicians could finally look at patient data themselves. That’s table stakes in this market; Nevro just didn’t have it yet.",
        ),
    ],
    "project/arrive-logistics/index.html": [
        (
            "Arrive's load board was stuck in the past—it looked like an Excel spreadsheet and functioned like one too. Carriers struggled to find critical shipping information while juggling hundreds of tabs and handling live customer calls. As lead UX designer, I partnered with internal carrier teams to understand their complex workflows through shadowing sessions and iterative user testing. Breaking from the typical \"mobile first\" approach, I prioritized desktop design since this tool was used exclusively by internal employees at their workstations. Through multiple design iterations and real-time feedback sessions, I created a modern, modular interface that prioritized information based on actual carrier decision-making patterns.",
            "Arrive’s load board was Excel with a login. Carriers hunted for shipping details while a customer was on the line. I shadowed them, tested on their desks, and designed for desktop — that’s where the work happens. A few full rewrites later, the layout followed how they actually decide, not how the spreadsheet was structured.",
        ),
        (
            "Arrive's load board looked and felt like an Excel spreadsheet from another era. For carriers managing hundreds of loads and switching between countless tabs, this outdated interface created real operational problems. During high-pressure customer calls, they needed to quickly locate specific shipping details, but the dense data tables made this unnecessarily difficult.",
            "The load board looked like a spreadsheet from another decade. Carriers sit on the phone with customers, flipping through hundreds of loads and a pile of tabs, trying to find one shipping detail before the other person gets impatient.",
        ),
        (
            "I started with extensive user research interviews with internal stakeholders—the carriers themselves. These conversations led to dozens of wireframes and detailed user flow maps. A carrier's workflow is remarkably complex, touching multiple systems and requiring constant context-switching. I needed to understand this process deeply before I could make it better.",
            "I started with interviews and a lot of wires. A carrier’s day touches more systems than you’d think, and they’re switching context the whole time.",
        ),
        (
            "The breakthrough came when I started shadowing carriers during actual calls. I sat beside them, watching not just what they told me, but what they actually did. This observational research revealed a crucial insight: their actions often told a different story than their words. They'd say one feature was important, but I'd watch them repeatedly use a workaround for something entirely different.",
            "The useful part was sitting next to them on live calls. People would tell me a feature mattered and then never touch it — they’d use a workaround instead.",
        ),
        (
            "Given the desktop-heavy nature of their work, I broke from the typical \"mobile first\" methodology and focused on desktop designs. Each iteration went through user testing sessions with real carriers, and their feedback directly shaped the next version. There were several complete revisions before we reached the final design—each one teaching us something new about how carriers actually worked.",
            "It’s a desktop job, so I skipped mobile-first and designed for the workstation. We threw away a few full versions. Each one taught us something the interviews hadn’t.",
        ),
        (
            "The redesigned load board transformed how carriers interact with shipping data. Instead of hunting through spreadsheet rows, I created a modern, modular interface that surfaced the right information at the right time.",
            "I stopped treating it like a grid of cells. The fields they actually used on calls sat up top. Everything else was still there, just quieter.",
        ),
        (
            "Information hierarchy became the foundation. By analyzing carrier workflows during those shadowing sessions, I understood which data points drove decisions. The new design prioritized these elements, making critical details immediately scannable while keeping secondary information accessible but not overwhelming.",
            "Shadowing told me which numbers actually drove a decision. Those got the attention. Secondary stuff stayed reachable.",
        ),
        (
            "The modular component system I designed reduced the need for constant tab-switching. Related information was grouped logically, following the natural flow of a carrier's decision-making process. Visual design played a supporting role—using contrast, spacing, and typography to create clear information zones rather than relying on grid lines like the old spreadsheet interface.",
            "Related info lived together so they weren’t hopping tabs for one decision. Contrast and type did the work the old grid lines used to do.",
        ),
        (
            "Flexibility was key. Different carriers had slightly different workflows, so the system needed to accommodate these variations without becoming cluttered or complex.",
            "Different carriers work a little differently, so it had to bend without turning into a junk drawer.",
        ),
        (
            "The impact showed up in daily operations. Carriers could process loads faster, especially during peak times when every second counted. The reduced cognitive load meant they could focus on customer conversations instead of fighting with the interface. During high-pressure calls, they could quickly find the information they needed and respond confidently. The modern interface didn't just look better—it fundamentally improved how carriers did their jobs.",
            "They could find a load faster, especially when the board was slammed. Less time fighting the tool, more time on the call.",
        ),
    ],
    "project/qualtrics/index.html": [
        (
            "Joining Qualtrics during its growth phase before the company's major expansion, I contributed to multiple high-impact areas of the product. My primary focus was transforming desktop survey creation tools into an effective mobile experience while maintaining enterprise-level functionality. I designed the mobile app nearly from scratch, including the complex \"Magic Link\" secure authentication system required post-acquisition. Collaborating with engineering teams in Krakow, Poland, I adapted dense desktop dashboards for mobile interfaces. Additionally, I inherited and completely redesigned the Create UI—the primary interface for survey creation—conducting rigorous user testing and creating high-fidelity prototypes that guided development and informed the product roadmap.",
            "I joined Qualtrics before the big expansion and spent most of my time on mobile — including Magic Link, which had to satisfy security after the acquisition — and on Create UI, the screen that starts every survey. Engineering was in Krakow. The mobile designs shipped. The Create UI prototypes were close to what went live.",
        ),
        (
            "Qualtrics faced a significant challenge: how do you transform complex, enterprise-level survey creation tools into a mobile experience without sacrificing functionality? Desktop dashboards packed with data and options needed to work on small screens. Additionally, post-acquisition security requirements demanded a sophisticated mobile authentication solution.",
            "Qualtrics is a dense desktop tool. We needed a mobile app that didn’t feel like a shrunk dashboard, plus a sign-in flow that would pass post-acquisition security.",
        ),
        (
            "I joined the team during an exciting growth phase and quickly became involved in multiple product areas. The mobile app became my primary focus, and I was essentially building it from scratch.",
            "The mobile app became mine, basically from scratch.",
        ),
        (
            "The \"Magic Link\" sign-in process was one of my first major challenges. Security was paramount—this wasn't a consumer app but an enterprise tool handling sensitive survey data. The authentication flow needed to be both secure and user-friendly, a difficult balance that required close collaboration with security teams.",
            "Magic Link was early and annoying in the right way: enterprise survey data, so security had opinions, and typing passwords on a phone is miserable. I worked that out with the security team.",
        ),
        (
            "Adapting desktop dashboards for mobile required a different mindset. I couldn't simply shrink desktop layouts—I needed to prioritize information and restructure interactions for touch interfaces and smaller screens. Working closely with engineers in Krakow, Poland, I created wireframes and mockups in Sketch (later transitioning to Figma) that guided development.",
            "I didn’t scale the desktop down. I picked what people actually need on a phone and rebuilt the rest for touch. Engineering was in Krakow. I was in Sketch, then Figma.",
        ),
        (
            "The Create UI project was different. I inherited this critical interface—the first thing users encounter when building surveys—and saw an opportunity to modernize it significantly. Whether users started from scratch or used templates, the Create UI shaped their entire experience.",
            "Create UI was a different job. I inherited the first screen of survey building — scratch or template — and it showed.",
        ),
        (
            "I developed high-fidelity prototypes that simulated real-world survey creation scenarios. User testing became crucial—I needed to understand how people actually created surveys, not just how I thought they should. Post-testing, I meticulously documented feedback, identifying patterns that informed both immediate design iterations and longer-term product roadmap planning.",
            "I made high-fidelity prototypes, tested them, and wrote down what kept coming up so it could feed the roadmap, not just the next mock.",
        ),
        (
            "The mobile app redesign delivered an intuitive experience that brought Qualtrics functionality to users on the go. The Magic Link authentication system balanced security requirements with user convenience—users could securely access their accounts without cumbersome password entry on mobile devices.",
            "Magic Link let people in without a password on their phone, and security signed off.",
        ),
        (
            "For mobile dashboards, I restructured information hierarchy to prioritize what users needed most frequently. Progressive disclosure patterns kept advanced features accessible without cluttering the initial view. Touch interactions felt natural, with appropriately sized tap targets and gestures that matched mobile conventions.",
            "Mobile dashboards lead with the frequent stuff. The rest is one tap further. Targets are actually tappable.",
        ),
        (
            "The upcoming \"Northstar\" designs will expand mobile functionality further, adding ticketing creation and maintenance features. These designs build on the foundation I established, maintaining consistency while adding capabilities users have requested.",
            "There’s a later “Northstar” pass for ticketing that builds on this.",
        ),
        (
            "The Create UI redesign transformed the survey creation experience. I modernized the aesthetic while improving the functional flow. Template selection became clearer, with better previews helping users choose starting points. The scratch-build process followed a more logical progression, reducing cognitive load during survey design.",
            "Create UI got a clearer template picker and a less confusing path if you start from zero. Power users didn’t lose the deep stuff; new users could find the front door.",
        ),
        (
            "The high-fidelity prototypes I created were detailed enough to guide engineering implementation closely. When the Create UI went live, it matched my prototypes remarkably well—a testament to thorough design specification and strong collaboration with the development team.",
            "Engineering built close to the prototypes. When Create UI went live, it looked like the files.",
        ),
        (
            "User feedback validated the redesign approach. The improved Create UI made survey creation more approachable, especially for new users, while maintaining the power features that experienced users relied on.",
            "New users had an easier time starting. Experienced users kept the power features.",
        ),
        (
            "The impact is ongoing. My mobile designs are now in production, serving Qualtrics customers daily. The Create UI redesign continues to evolve based on the research and design foundation I established. Being part of Qualtrics during its growth phase, contributing to products that thousands of enterprise customers use, was particularly rewarding. The fidelity between my prototypes and the live implementations demonstrated the value of thorough design process and effective collaboration.",
            "The mobile work is in the production app. Create UI kept evolving from that research after I moved on.",
        ),
    ],
    "project/punchh/index.html": [
        (
            "As Lead Mobile UX Designer at Punchh, I owned the complete redesign of our white-label mobile framework—the foundation for hundreds of restaurant apps across the country. The pandemic had accelerated mobile delivery adoption, but our dated interface risked losing restaurant clients to competitors offering superior experiences. The unique challenge was designing a system that could be customized for diverse restaurant needs (from reward redemption to complex food ordering) while maintaining a consistent, modern foundation. Through competitive analysis, user research, and extensive prototyping, I created a contemporary framework that matched industry leaders while preserving the flexibility our restaurant clients required.",
            "I was lead mobile designer at Punchh and I owned the white-label app framework — the thing behind hundreds of restaurant apps. Delivery took off during COVID and our UI looked old. The job was one system that could look like a national chain or a neighborhood place without falling apart underneath.",
        ),
        (
            "Punchh's white-label mobile framework powered hundreds of restaurant apps, but we had a problem: our interface looked dated compared to competitors. This became critical during the pandemic when mobile delivery orders surged and restaurants needed apps that matched user expectations set by industry leaders.",
            "Punchh’s framework powered a few hundred restaurant apps and looked tired. Then the pandemic hit and delivery became the business. Brands started comparing us to everyone else.",
        ),
        (
            "The white-label model presented unique design challenges. Our framework served everyone from quick-service chains to upscale restaurants, each with different needs. Some had complex reward systems; others needed extensive food customization options. The framework had to be flexible enough to accommodate these variations while maintaining usability and modern aesthetics.",
            "White-label is the whole problem. A QSR and a sit-down place don’t want the same app. Some care about points, some about modifiers. One system had to cover that without looking generic.",
        ),
        (
            "As the sole mobile designer, I owned the entire mobile product from research to final UI. I started with competitive analysis, studying leading restaurant apps to understand what \"modern\" meant in this space. I wasn't looking to copy—I needed to understand the patterns and features that users had come to expect.",
            "I was the only mobile designer. I looked at the apps people already liked — not to copy them, just to see what had become expected.",
        ),
        (
            "User research studies revealed diverse dining patterns and preferences across different restaurant types. I created detailed wireframes mapping various user journeys—from discovering deals to customizing orders to redeeming rewards. Flow charts helped me visualize how different restaurant types would implement the framework.",
            "Then I wired out deals, customization, rewards. A lot of restaurant types, a lot of paths.",
        ),
        (
            "The prototyping phase was iterative. I designed multiple UI variations and presented them for stakeholder review, balancing aesthetic modernization with the practical constraints of white-label customization. Each iteration tested different approaches to solving the \"one framework, many brands\" problem.",
            "A lot of UI versions. Stakeholders picked apart each one. The question was always: can another brand skin this without breaking it?",
        ),
        (
            "The redesigned framework delivered a contemporary interface that finally matched our competitors while solving the white-label customization challenge.",
            "I split the bones from the brand.",
        ),
        (
            "I built a modular component system that separated brand-neutral structure from customizable brand elements. The core interaction patterns—navigation, content hierarchy, action buttons—followed modern mobile conventions. These provided the contemporary feel users expected. Brand customization points (colors, logos, imagery, specific menu structures) could be adapted without breaking the underlying usability.",
            "Navigation, hierarchy, buttons stayed consistent. Color, logo, photos, menu shape could move.",
        ),
        (
            "The framework accommodated varied reward systems through flexible component designs. Whether a restaurant used points-based rewards, punch cards, or tiered memberships, the interface adapted while maintaining consistency. Food customization flows worked similarly—the framework supported everything from simple \"add-ons\" to complex build-your-own configurations.",
            "Rewards could be points, punch cards, or tiers. Food customization could be “add bacon” or a full builder. Same frame.",
        ),
        (
            "I integrated features users expected from leading food delivery apps: clear nutritional information, saved favorites, easy reordering, and intuitive checkout flows. These weren't just visual additions—each feature was designed to work within the white-label structure.",
            "I put in the stuff people now expect: nutrition, favorites, reorder, a checkout that doesn’t fight you.",
        ),
        (
            "The impact came at a critical moment. As pandemic-driven delivery orders surged, restaurants using Punchh could offer their customers a mobile experience on par with industry leaders. The framework supported their growth without forcing them to sacrifice brand identity. Restaurants maintained their unique look and feel while benefiting from contemporary UX patterns.",
            "Restaurants using Punchh could look current without giving up how they look.",
        ),
        (
            "For Punchh, the redesign moved us from \"functional at minimum\" to genuinely competitive. During a period when restaurants were evaluating their technology partners, we could demonstrate a modern mobile experience that met rising user expectations.",
            "For Punchh it was the difference between “fine” and “we can keep this account.”",
        ),
    ],
    "project/vodii-flueid/index.html": [
        (
            "At Vodii, I wore multiple hats as the sole designer—UX designer, visual designer, front-end developer, and project manager. The TxM software for real estate document management was built on an aging framework that limited both functionality and user productivity. Home buyers and stakeholders struggled with inefficient document signing and sharing processes. Despite operating in a niche market with limited competition, the outdated technology threatened our ability to grow. I led the complete redesign, leveraging my full-stack background to not only design but also implement the front-end code. The result was a modern, modular platform that transformed TxM from a legacy system into scalable infrastructure ready for Vodii's next growth phase.",
            "At Vodii I was the designer, the front-end, and the project manager. TxM handled real estate documents on a stack that couldn’t take new work. I redesigned it and built the front-end. After Flueid acquired the company, the new system was what they kept building on.",
        ),
        (
            "Vodii's TxM platform had a fundamental problem: it was built on outdated technology that couldn't keep up with evolving digital expectations. Home buyers and real estate stakeholders needed to sign and share documents efficiently, but the aging framework made simple tasks unnecessarily complicated.",
            "TxM was how home buyers and real estate folks signed and shared documents, and the stack was old. Simple tasks took too many steps.",
        ),
        (
            "Operating in a niche market meant we didn't face intense competition, but that created its own challenge. Without competitive pressure driving innovation, the platform had stagnated. However, to grow the product and meet modern user expectations, we needed to completely overhaul the technology infrastructure.",
            "It’s a niche, so nobody was breathing down our neck. That’s how a product sits still. If we wanted it to grow, the foundation had to be rebuilt.",
        ),
        (
            "As the solo designer (and one of only two design team members post-acquisition by Flueid), I took on an unusually broad role. I wasn't just designing interfaces—I was managing the project timeline, making technical decisions, and implementing front-end code. My background in front-end web development became essential.",
            "I was the only designer (two of us after Flueid bought Vodii). I also ran the timeline, made technical calls, and wrote front-end. That’s the job when the team is that small.",
        ),
        (
            "I started by thoroughly assessing the existing platform's technical and UX limitations. What could be improved within the current framework? What required complete rebuilds? These decisions shaped the project scope and timeline.",
            "First pass: what can we save, what do we throw out.",
        ),
        (
            "The design process focused on creating a modern, modular architecture. \"Modular\" was key—the new system needed to support feature additions without requiring major overhauls each time. I designed components that could be reused and recombined, building flexibility into the foundation.",
            "Then a modular setup so the next feature didn’t mean another rewrite.",
        ),
        (
            "Throughout development, I balanced technical constraints with user needs. Working alone meant I could move quickly, but it also meant carefully prioritizing what mattered most. I focused on streamlining the core document workflows—signing, sharing, tracking—while building infrastructure that could support future features.",
            "Working alone is fast until you pick the wrong thing. Signing, sharing, tracking first. Fancy later.",
        ),
        (
            "The redesigned TxM platform replaced the legacy system with contemporary technology and user experience. The interface transformation was immediately visible—clean, modern screens replaced outdated layouts—but the real improvements ran deeper.",
            "New UI, yes — but the useful part was the structure.",
        ),
        (
            "I built a modular architecture that separated concerns and created reusable components. Document workflows became more intuitive, reducing the steps required for common tasks. Home buyers could sign documents more easily, and real estate professionals could manage multiple transactions without fighting the interface.",
            "Common document tasks took fewer steps. Buyers could sign without a scavenger hunt; agents could run more than one transaction without fighting the tool.",
        ),
        (
            "The design system I created provided consistency across the platform while supporting future expansion. New features could be built using existing components, accelerating development and maintaining UX coherence.",
            "I built a design system I could keep adding to.",
        ),
        (
            "As both designer and front-end developer, I could ensure the implementation matched the design vision. There was no \"lost in translation\" gap between design files and live code—I controlled both, making real-time adjustments as technical realities emerged.",
            "Because I was writing the front-end, the file and the browser didn’t drift apart.",
        ),
        (
            "The technical infrastructure became more maintainable and scalable. The modular approach meant future developers could work on specific features without untangling complex dependencies.",
            "Later people could touch one feature without untangling the whole thing.",
        ),
        (
            "The impact extended beyond immediate usability improvements. The modernized platform positioned Vodii for sustainable growth with technology that could support years of feature development. When Flueid acquired Vodii, the redesigned TxM system became the foundation for the combined company's continued development.",
            "After Flueid acquired Vodii, this was still the base.",
        ),
        (
            "For users, the platform finally met modern expectations for digital document management. For the business, it transformed a liability (aging technology) into an asset (scalable infrastructure). The redesign successfully bridged Vodii's past and future.",
            "Aging software stopped being the thing we apologized for.",
        ),
    ],
    "project/tripping/index.html": [
        (
            "In my time at Tripping, I took on the challenge of redesigning Tripping's entire vacation rental platform as the sole designer on the team. The product had never received dedicated UX attention, requiring a complete overhaul from homepage to listing pages. Working with my manager, I crafted a modern interface that presented rental information clearly while ensuring scalability across mobile and desktop. An unexpected challenge emerged: user-contributed photos varied wildly in quality, degrading the browsing experience. Collaborating with engineering, we implemented an innovative machine learning solution that ranked and displayed images by quality, resulting in measurable improvements in engagement and conversion rates.",
            "First UX job. I redesigned Tripping’s vacation rental site — homepage through listings — with my manager. User photos were all over the place, so I worked with engineering on ML ranking to put the better shots first. That did more for engagement than a lot of the visual polish.",
        ),
        (
            "Tripping needed help. As a vacation rental platform, it competed in a crowded marketplace, but the site had never received dedicated UX design attention. Every page—from the homepage through search results to individual listings—needed a complete redesign.",
            "Tripping had never had a dedicated UX designer. Homepage, search, listings — all of it needed a pass.",
        ),
        (
            "This was my first UX role, and the responsibility was significant. As the sole designer (aside from my manager), I would directly impact the entire user experience. The challenge was exciting and somewhat daunting.",
            "This was my first UX role. I was the only designer besides my manager.",
        ),
        (
            "I started with a comprehensive UX audit, identifying the most critical areas for improvement. The vacation rental search and discovery process needed to work seamlessly—users comparing multiple properties had to quickly assess options and find the right fit. Information density was a key consideration: rental listings contain lots of details (amenities, pricing, location, availability), but overwhelming users would hurt conversion.",
            "Search is the product: compare a pile of rentals without drowning in amenities and prices.",
        ),
        (
            "The interface needed to work across mobile and desktop. More users were searching for rentals on mobile devices, but desktop still dominated bookings. The responsive design had to accommodate both contexts without compromising either experience.",
            "More people browsed on phones; bookings still happened on desktop. Both had to work.",
        ),
        (
            "During the redesign process, an unexpected problem surfaced through user research: photo quality. Unlike major platforms like Airbnb with professional photography, Tripping relied on user-contributed images. Quality varied dramatically—some properties had beautiful photos, others had dark, blurry, or poorly composed images. Poor photos degraded the browsing experience and likely hurt conversion rates, even for properties that were actually great.",
            "The surprise was photos. These aren’t Airbnb shoots. Hosts upload whatever. Dark, blurry, one good picture buried at the end.",
        ),
        (
            "This became an opportunity for creative problem-solving. Working with our engineering team, we explored using machine learning to rank images by quality. The ML system could analyze photos and display the best ones first, giving each property the strongest possible first impression.",
            "We started ranking images with ML so the decent ones showed up first.",
        ),
        (
            "The redesigned platform delivered a modern, scalable interface that transformed how users discovered vacation rentals on Tripping.",
            "Homepage gets you into search.",
        ),
        (
            "The homepage established clear visual hierarchy and guided users into search quickly. I designed the search and filtering experience to help users narrow options efficiently without feeling overwhelmed by choices. Rental information architecture became more scannable—key details like price, location, and standout amenities were immediately visible, with additional details accessible when users wanted to dive deeper.",
            "Filters narrow without a wall of options. Price, place, and the one or two amenities that matter sit up front.",
        ),
        (
            "The responsive design adapted intelligently between mobile and desktop. On mobile, I prioritized browsing efficiency and quick property comparisons. Desktop layouts took advantage of larger screens to show more detail and enable easier multi-property comparison.",
            "Mobile is for browsing and comparing quickly. Desktop shows more at once.",
        ),
        (
            "The ML-powered image ranking solution was particularly impactful. Instead of displaying user-uploaded photos in arbitrary order, the system analyzed and ranked images by quality. Properties were now represented by their best photos first—well-lit, properly composed images that showcased spaces effectively. This seemingly simple change had measurable effects on user engagement.",
            "The photo ranking was the part people felt. Same listings, better first impression.",
        ),
        (
            "Visual design modernized the entire platform. Clean layouts, contemporary typography, and thoughtful use of whitespace made the information-dense content more digestible. The interface felt current and trustworthy, essential qualities in the vacation rental marketplace where users are committing significant money to properties they haven't seen in person.",
            "The rest was a cleaner layout so a page full of details didn’t feel like a spreadsheet. People are about to spend real money on a place they haven’t stood in.",
        ),
        (
            "The redesign improved both engagement metrics and conversion rates. The ML image ranking was particularly effective—properties looked better, users browsed longer, and more browsing sessions converted to bookings. The modern interface helped Tripping compete more effectively in a marketplace dominated by larger, better-funded competitors.",
            "Engagement and conversion both moved. I don’t have the exact numbers in front of me anymore, so I’m not going to invent them. The photos did more of that work than the type.",
        ),
        (
            "For me personally, this project was formative. As my first UX role, it taught me how to lead a comprehensive redesign, balance competing priorities, and collaborate with engineering on creative solutions to unexpected problems. The image quality challenge—and our ML solution—demonstrated that good UX design sometimes means solving problems that aren't immediately obvious in the initial brief.",
            "The brief didn’t mention the photos. That’s usually how it goes.",
        ),
        (">Mobile Design<", ">UX design<"),
    ],
}

IMAGE_ALTS = {
    "GzrKyyw6f76IaiED3HTTxklQs8.jpeg": "Claritea reading app",
    "luReBf9uh5DGHWwN9NtGeiXbc.png": "Nevro patient monitoring",
    "vQOIjwfgX3rw1B1hMDOAMJ53Dk.png": "Arrive Logistics load board",
    "BBhiDIVtxXWjdiOq3GnFVaXHHg.png": "Qualtrics survey product",
    "U3SF1uu0hMvFfLbmMtC34gKX9Gk.png": "Punchh restaurant app",
    "wPE6ZP7EW3tYMYYBK8JWtZZAU.png": "Vodii document platform",
    "s208M45ZoNa6Cs3dGcwWp9Q5Tk8.png": "Tripping vacation rentals",
}

NEW_LISTING = [
    (
        "punchh",
        "Punchh",
        "White-label restaurant apps for hundreds of brands. I rebuilt the mobile framework when delivery exploded during COVID.",
        "One framework, a lot of brand skins. Sole mobile designer.",
        "U3SF1uu0hMvFfLbmMtC34gKX9Gk.png",
        "Punchh restaurant app",
    ),
    (
        "vodii-flueid",
        "Vodii (Flueid)",
        "Real estate document tool on aging tech. I redesigned TxM and wrote the front-end — it stuck around after Flueid bought the company.",
        "Solo designer. Signing, sharing, tracking — then a system that could take new features.",
        "wPE6ZP7EW3tYMYYBK8JWtZZAU.png",
        "Vodii document platform",
    ),
    (
        "tripping",
        "Tripping",
        "First UX job. I redesigned the vacation rental site, then ranked listing photos with ML because the uploads were a mess.",
        "Engagement and conversion went up. The photo ranking did more than the new type.",
        "s208M45ZoNa6Cs3dGcwWp9Q5Tk8.png",
        "Tripping vacation rentals",
    ),
]


def add_missing_listing_cards(html: str) -> str:
    if 'href="./project/punchh"' in html:
        return html
    match = re.search(
        r'<a class="framer-6ramz1 framer-1yjdw9l" href="\./project/qualtrics".*?</a><!--/\$-->',
        html,
        flags=re.DOTALL,
    )
    if not match:
        print("  ! could not find Qualtrics listing card")
        return html
    template = match.group(0)
    extras = []
    for slug, title, blurb, overlay, filename, alt in NEW_LISTING:
        card = template
        card = card.replace("./project/qualtrics", f"./project/{slug}")
        card = card.replace("Qualtrics", title)
        card = card.replace(
            "Mobile app, Magic Link sign-in, and the Create UI that starts every survey. The mobile work is in the live product.",
            blurb,
        )
        card = card.replace(
            "Worked with engineering in Krakow. Prototypes that actually matched what shipped.",
            overlay,
        )
        # If copy rewrite hasn't landed yet, also replace originals.
        card = card.replace(
            "Transforming complex desktop survey tools into an intuitive mobile experience while redesigning the critical Create UI interface used by thousands of enterprise customers.",
            blurb,
        )
        card = card.replace(
            "My mobile designs are now live in the production app, providing Qualtrics users with on-the-go access to essential features. The Create UI redesign improved the critical first interaction users have with the platform, with high-fidelity prototypes closely matching the eventual live implementation.",
            overlay,
        )
        card = card.replace("BBhiDIVtxXWjdiOq3GnFVaXHHg.png", filename)
        card = card.replace("Stylish Modern Wristwatch", alt)
        card = set_image_alt(card, filename, alt)
        extras.append(card)
    return html[: match.end()] + "".join(extras) + html[match.end() :]


def rewrite_file(path: Path) -> None:
    rel = str(path.relative_to(ROOT))
    html = path.read_text(encoding="utf-8")
    original = html

    html = replace_all(html, GLOBAL_PAIRS)
    html = replace_all(html, FAQ_PAIRS)
    html = replace_all(html, SKILL_PAIRS)
    html = replace_all(html, CARD_PAIRS)
    html = replace_all(html, CASE_PAIRS.get(rel, []))

    for old, new in SPLIT_BY_FILE.get(rel, []):
        html = replace_split(html, old, new)

    for filename, alt in IMAGE_ALTS.items():
        html = set_image_alt(html, filename, alt)

    if rel == "project/index.html":
        html = add_missing_listing_cards(html)

    if html != original:
        path.write_text(html, encoding="utf-8")
        print(f"updated {rel} ({len(html) - len(original):+d} chars)")
    else:
        print(f"unchanged {rel}")


def main() -> None:
    files = [
        ROOT / "index.html",
        ROOT / "about/index.html",
        ROOT / "project/index.html",
        ROOT / "404.html",
    ]
    files.extend(sorted((ROOT / "project").glob("*/index.html")))
    for path in files:
        rewrite_file(path)


if __name__ == "__main__":
    main()
