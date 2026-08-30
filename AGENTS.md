# Jasmine Wilson portfolio

Static self-hosted copy of jasminewilson.com. Framer HTML plus `overrides.css` / `overrides.js`.

## Run

```bash
npm start
```

http://localhost:3000/ — hard-refresh after CSS/JS changes.

Pages: `/`, `/about`, `/project`, and case studies under `/project/{claritea,nevro,arrive-logistics,qualtrics,punchh,vodii-flueid,tripping}`.

## Copy and layout

- Do not invent metrics or restyle the chrome.
- Visible copy often lives in huge minified HTML lines or letter-split spans. Prefer a Python string/split-text replace over grep.
- Framer hydration stays off. Mobile/tablet Menu is handled in `overrides.js`. Skip `[data-framer-name="Nav Content"]` in any reveal/unhide helper.
- Skip Overlay nodes so project-card overlays stay hidden.

## Cursor Cloud specific instructions

- The site is static. `npm start` serves it on port 3000.
- Verify UI changes in the browser at desktop, tablet (~1024), and phone (~390).
- Push to `main` deploys on Vercel (`jasmine-wilson-portfolio`).
