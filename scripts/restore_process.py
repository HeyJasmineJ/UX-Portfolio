#!/usr/bin/env python3
"""Put process detail back into case studies and project cards."""

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

PAIRS: list[tuple[str, str]] = [
    ("The problem", "Research & process"),
    ("What I made", "What shipped"),
    # --- homepage / listing cards ---
    (
        "A reading app I designed and built. Sessions, not streaks — and a Focus Score from heart rate, not guilt.",
        "I interviewed ADHD and wellness readers, then designed and built a session-based reading app — Focus Score from heart rate, not a yearly streak.",
    ),
    (
        "I designed and built the whole thing — app, Mac companion, waitlist.",
        "Interviews → principles → HTML prototype → React Native, HealthKit, and a Mac companion.",
    ),
    (
        "Remote monitoring for pain patients. Physicians could finally see implant data without waiting on the company.",
        "I sat with physicians in clinic, then designed the HCP Portal, patient app, and design system so they could monitor implants themselves.",
    ),
    (
        "First in-house designer. Portal, patient app, and a design system. The MVP shipped in the US.",
        "Usability studies and clinical observation. Sole designer. Portal, mobile, front-end, regulatory docs. MVP shipped in the US.",
    ),
    (
        "The load board used to look like Excel. I sat with carriers on live calls and redesigned it so they could find a load mid-sentence.",
        "I shadowed carriers on live calls. What they did and what they said didn’t match — the new board followed the workarounds.",
    ),
    (
        "Desktop-first. A few full rewrites. Faster to scan when the board is slammed.",
        "Interviews, wires, then desk-side testing. Desktop-first. A few full layouts thrown out before the hierarchy stuck.",
    ),
    (
        "Mobile app, Magic Link sign-in, and the Create UI that starts every survey. The mobile work is in the live product.",
        "I designed mobile almost from scratch — Magic Link with security, dashboards rebuilt for touch — and redesigned Create UI after testing how people actually start a survey.",
    ),
    (
        "Worked with engineering in Krakow. Prototypes that actually matched what shipped.",
        "Sketch then Figma, engineers in Krakow, high-fidelity prototypes. Mobile shipped; Create UI landed close to the files.",
    ),
    (
        "White-label restaurant apps for hundreds of brands. I rebuilt the mobile framework when delivery exploded during COVID.",
        "Sole mobile designer. Competitive audit, then a white-label system that could do points or punch cards, simple add-ons or a full builder.",
    ),
    (
        "One framework, a lot of brand skins. Sole mobile designer.",
        "A lot of UI versions. The test was always: can another brand skin this without breaking checkout, rewards, or the order flow?",
    ),
    (
        "Real estate document tool on aging tech. I redesigned TxM and wrote the front-end — it stuck around after Flueid bought the company.",
        "I audited what we could keep, rebuilt the rest, and wrote the front-end. Signing, sharing, tracking first — then a system that could take new features.",
    ),
    (
        "Solo designer. Signing, sharing, tracking — then a system that could take new features.",
        "Solo designer, also PM and front-end. Modular components so the next feature didn’t mean another rewrite. Flueid kept building on it.",
    ),
    (
        "First UX job. I redesigned the vacation rental site, then ranked listing photos with ML because the uploads were a mess.",
        "First UX role. I audited homepage through listings, then worked with engineering to rank host photos with ML so the first image wasn’t a dark kitchen.",
    ),
    (
        "Engagement and conversion went up. The photo ranking did more than the new type.",
        "UX audit, then search IA and responsive layouts. The photo ranking moved engagement more than the visual polish.",
    ),
    # --- claritea ---
    (
        "The map was pretty clear: Bookly and Basmo count minutes, Fable and Goodreads do community, wellness apps ignore books. Nobody sat at",
        "I mapped the competitors: Bookly and Basmo count minutes; Fable and Goodreads do community; wellness apps ignore books. Nothing sat at",
    ),
    (
        "I prototyped the core loop in HTML (navigation, session, spoilers, Focus Score), then built it in React Native (Expo) with Supabase and a SwiftUI Mac companion. This isn’t only screens.",
        "I prototyped the core experience in a high-fidelity HTML prototype — navigation, session flow, spoiler states, Focus Score reveal — then implemented it in React Native (Expo) with a shared Supabase backend and a native SwiftUI Mac companion. The case study isn’t only screens; it’s a working system.",
    ),
    (
        "A reading app I designed and built. Sessions, not streaks — and a Focus Score from heart rate, not guilt. I designed and built it as a personal, production-ready product that connects reading sessions to biometric signals (heart rate, HRV via Apple HealthKit / Health Connect) and turns that into a Focus Score: a clear, humane signal of how reading lands in the body. The experience is ADHD-first—check-ins, pacing, and focus tools that support attention without shame—alongside a Mac companion and waitlist-facing marketing.",
        "Claritea treats reading as nervous-system care, not a catalog or a streak contest. I interviewed aspirational, ADHD, and wellness readers, set principles from those conversations, prototyped the session loop, and built the product: React Native, HealthKit / Health Connect biometrics, a Focus Score, ADHD-first check-ins, a Mac companion, and a waitlist. Personal project. It runs.",
    ),
    (
        "Claritea treats reading as nervous-system care, not a catalog or a streak contest. I designed and built it: sessions tied to heart rate and HRV (HealthKit / Health Connect), turned into a Focus Score — how the reading landed in the body, not how many books you owed the year. ADHD-first check-ins and pacing, a Mac companion, and a waitlist. Personal project. It runs.",
        "Claritea treats reading as nervous-system care, not a catalog or a streak contest. I interviewed aspirational, ADHD, and wellness readers, set principles from those conversations, prototyped the session loop, and built the product: React Native, HealthKit / Health Connect biometrics, a Focus Score, ADHD-first check-ins, a Mac companion, and a waitlist. Personal project. It runs.",
    ),
    # --- nevro ---
    (
        "I was the only designer. I sat with physicians, watched them use the devices in clinic, and ran usability studies. What they needed was pretty plain: patient data without a scavenger hunt, trends over time, and something that fit the visit — not a new workflow.",
        "I was the only designer. I ran usability studies and sat with physicians while they used the Programmer and the existing app in clinic. The gaps weren’t in a spec: they needed the last session, a trend over time, and a way to jump to the patient who needed a call — during the visit, not after. Tools had to fit the appointment, not invent a new one.",
    ),
    (
        "Then I mapped the portal, the mobile app, and the physician tools. Healthcare regs, security, and the fact that these things talk wirelessly to an implant all shaped what we could ship.",
        "The HCP Portal, patient app, and Programmer had been designed as separate products. I mapped how data had to move between them. Healthcare regs, security, and wireless talk to an implant all shaped what we could actually ship.",
    ),
    (
        "The HCP Portal was the main one — a web dashboard for one patient or a whole panel. Urgent stuff up front; they could drill in when they needed to.",
        "The HCP Portal was the centerpiece — a web dashboard for one patient or a whole panel. I designed visualizations to spot who needed attention, kept urgent data up front, and put history one click in.",
    ),
    (
        "The patient app got a real connection to the implant so people could log pain and their physician could see it without extra steps.",
        "The patient app got a real connection to the implant so people could log pain in the moment and their physician could see it without a separate upload.",
    ),
    (
        "I also designed and coded a design system — components for mobile, desktop, and email — and handed the base pieces to engineering.",
        "I designed and coded a design system for mobile, desktop, and email, then handed the base components to engineering so the three surfaces didn’t drift.",
    ),
    (
        "I was Nevro’s first in-house designer. Physicians had no way to monitor implant patients unless the company sent them an update — competitors already had this. I did the research in clinic, then designed the HCP Portal, the patient app connection, and the design system. Front-end and the regulatory docs were part of the job.",
        "I was Nevro’s first in-house designer. Physicians couldn’t monitor implant patients unless the company sent an update — competitors already had remote monitoring. I did usability studies and clinic observation, mapped the portal / patient app / Programmer as one system, then designed and built the HCP Portal, the app connection, and a design system. Front-end and the regulatory documentation were part of the job.",
    ),
    # --- arrive ---
    (
        "I started with interviews and a lot of wires. A carrier’s day touches more systems than you’d think, and they’re switching context the whole time.",
        "I started with interviews and dozens of wires and flow maps. A carrier’s day touches more systems than you’d think, and they’re switching context the whole time. I needed that map before I changed the board.",
    ),
    (
        "The useful part was sitting next to them on live calls. People would tell me a feature mattered and then never touch it — they’d use a workaround instead.",
        "The useful part was sitting next to them on live calls. I watched what they did, not just what they told me. They’d say a feature mattered and then never touch it — they’d use a workaround instead. That became the design brief.",
    ),
    (
        "It’s a desktop job, so I skipped mobile-first and designed for the workstation. We threw away a few full versions. Each one taught us something the interviews hadn’t.",
        "It’s a desktop job, so I skipped mobile-first and designed for the workstation. Each version went back to carriers at their desks the same week. We threw away a few complete layouts. Interviews hadn’t caught what those sessions did.",
    ),
    (
        "Related info lived together so they weren’t hopping tabs for one decision. Contrast and type did the work the old grid lines used to do.",
        "Related fields lived together so they weren’t hopping tabs for one decision. I used contrast, spacing, and type to make zones — not more grid lines.",
    ),
    (
        "Arrive’s load board was Excel with a login. Carriers hunted for shipping details while a customer was on the line. I shadowed them, tested on their desks, and designed for desktop — that’s where the work happens. A few full rewrites later, the layout followed how they actually decide, not how the spreadsheet was structured.",
        "Arrive’s load board was Excel with a login. Carriers hunted shipping details while a customer was on the line. I interviewed them, mapped the flows, then shadowed live calls — what they did didn’t match what they said. I designed desktop-first, tested at their desks, and threw out a few full versions. The layout ended up following how they actually decide, not how the spreadsheet was structured.",
    ),
    # --- qualtrics ---
    (
        "The mobile app became mine, basically from scratch.",
        "I joined during a growth stretch. The mobile app became mine, basically from scratch.",
    ),
    (
        "I didn’t scale the desktop down. I picked what people actually need on a phone and rebuilt the rest for touch. Engineering was in Krakow. I was in Sketch, then Figma.",
        "I didn’t scale the desktop down. I picked what people actually open on a phone and rebuilt the rest for touch — progressive disclosure for the deep stuff. Engineering was in Krakow. I was in Sketch, then Figma.",
    ),
    (
        "I made high-fidelity prototypes, tested them, and wrote down what kept coming up so it could feed the roadmap, not just the next mock.",
        "I built high-fidelity prototypes that walked through real survey-creation scenarios, tested them, and wrote up the patterns so they could feed the roadmap — not just the next mock.",
    ),
    (
        "There’s a later “Northstar” pass for ticketing that builds on this.",
        "A later “Northstar” pass adds ticketing on top of this foundation, so mobile isn’t a read-only slice of the desktop product.",
    ),
    (
        "I joined Qualtrics before the big expansion and spent most of my time on mobile — including Magic Link, which had to satisfy security after the acquisition — and on Create UI, the screen that starts every survey. Engineering was in Krakow. The mobile designs shipped. The Create UI prototypes were close to what went live.",
        "I joined Qualtrics before the big expansion. I designed mobile almost from scratch, including Magic Link with the security team after the acquisition, and rebuilt desktop dashboards for touch with engineers in Krakow. I also inherited Create UI — the first screen of survey building — tested how people actually start a survey, and handed over prototypes close to what shipped.",
    ),
    # --- punchh ---
    (
        "I was the only mobile designer. I looked at the apps people already liked — not to copy them, just to see what had become expected.",
        "I was the only mobile designer, research through final UI. I started with a competitive audit of the restaurant apps people already used — not to copy them, to see which patterns had become expected.",
    ),
    (
        "Then I wired out deals, customization, rewards. A lot of restaurant types, a lot of paths.",
        "Then I wired the journeys: find a deal, customize an order, redeem a reward. Flow charts for how a QSR vs a sit-down place would implement the same framework.",
    ),
    (
        "A lot of UI versions. Stakeholders picked apart each one. The question was always: can another brand skin this without breaking it?",
        "A lot of UI versions. Stakeholders picked apart each one. The question was always: can another brand skin this without breaking checkout, rewards, or the order flow?",
    ),
    (
        "I was lead mobile designer at Punchh and I owned the white-label app framework — the thing behind hundreds of restaurant apps. Delivery took off during COVID and our UI looked old. The job was one system that could look like a national chain or a neighborhood place without falling apart underneath.",
        "I was lead mobile designer at Punchh and owned the white-label framework behind hundreds of restaurant apps. Delivery took off during COVID and our UI looked old. I ran a competitive audit, mapped deals / customize / rewards across restaurant types, and prototyped until one system could look like a national chain or a neighborhood place without breaking underneath.",
    ),
    # --- vodii ---
    (
        "First pass: what can we save, what do we throw out.",
        "First pass was an audit: what could we keep inside the old framework, and what had to be rebuilt. That set the scope and the timeline.",
    ),
    (
        "Then a modular setup so the next feature didn’t mean another rewrite.",
        "Then a modular architecture — reusable components so the next feature didn’t mean another rewrite.",
    ),
    (
        "Working alone is fast until you pick the wrong thing. Signing, sharing, tracking first. Fancy later.",
        "Working alone is fast until you pick the wrong thing. I kept the first release to signing, sharing, and tracking, and left room in the system for what came next.",
    ),
    (
        "At Vodii I was the designer, the front-end, and the project manager. TxM handled real estate documents on a stack that couldn’t take new work. I redesigned it and built the front-end. After Flueid acquired the company, the new system was what they kept building on.",
        "At Vodii I was the designer, the front-end, and the project manager. TxM handled real estate documents on a stack that couldn’t take new work. I audited what to keep, rebuilt the document workflows, designed a modular system, and implemented the front-end. After Flueid acquired the company, that system is what they kept building on.",
    ),
    # --- tripping ---
    (
        "Tripping had never had a dedicated UX designer. Homepage, search, listings — all of it needed a pass.",
        "Tripping had never had a dedicated UX designer. I started with an audit of homepage, search, and listings. All of it needed a pass.",
    ),
    (
        "Search is the product: compare a pile of rentals without drowning in amenities and prices.",
        "Search is the product: people compare a pile of rentals and drown in amenities, prices, location, and availability. I had to make that scannable without hiding the details they need to book.",
    ),
    (
        "The surprise was photos. These aren’t Airbnb shoots. Hosts upload whatever. Dark, blurry, one good picture buried at the end.",
        "Research surfaced a problem that wasn’t in the original brief: photos. These aren’t Airbnb shoots. Hosts upload whatever — dark, blurry, one good picture buried at the end. Even a great place looked bad.",
    ),
    (
        "We started ranking images with ML so the decent ones showed up first.",
        "I worked with engineering on a machine-learning ranker so the first photo wasn’t arbitrary. Better-lit, better-composed images moved to the front.",
    ),
    (
        "First UX job. I redesigned Tripping’s vacation rental site — homepage through listings — with my manager. User photos were all over the place, so I worked with engineering on ML ranking to put the better shots first. That did more for engagement than a lot of the visual polish.",
        "First UX job, only designer besides my manager. I audited and redesigned homepage through listings for mobile and desktop, then worked with engineering on ML ranking for host photos — the brief hadn’t mentioned that, and it did more for engagement than a lot of the visual polish.",
    ),
]


def main() -> None:
    files = [
        ROOT / "index.html",
        ROOT / "about/index.html",
        ROOT / "project/index.html",
    ]
    files.extend(sorted((ROOT / "project").glob("*/index.html")))
    for path in files:
        html = path.read_text(encoding="utf-8")
        original = html
        for old, new in PAIRS:
            html = html.replace(old, new)
        if html != original:
            path.write_text(html, encoding="utf-8")
            print(f"updated {path.relative_to(ROOT)}")
        else:
            print(f"unchanged {path.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
