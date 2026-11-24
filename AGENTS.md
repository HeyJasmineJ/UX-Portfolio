# Jasmine Wilson portfolio

Static HTML/CSS/JS site for jasminewilson.com.

## Run

```bash
npm start
```

http://localhost:3000/ — hard-refresh after CSS/JS changes.

Pages: `/`, `/about`, `/project`, and case studies under `/project/{claritea,nevro,arrive-logistics,qualtrics,punchh,vodii-flueid,tripping}`.

## Copy and layout

- Do not invent metrics.
- Shared markup comes from `scripts/render_site.py`. After copy changes, run `python3 scripts/render_site.py`.
- Verify UI at desktop, tablet (~1024), and phone (~390).
- Push to `main` deploys on Vercel (`jasmine-wilson-portfolio`).

## Cursor Cloud specific instructions

- The site is static. `npm start` serves it on port 3000.
- Verify UI changes in the browser at desktop, tablet (~1024), and phone (~390).
- Push to `main` deploys on Vercel (`jasmine-wilson-portfolio`).
