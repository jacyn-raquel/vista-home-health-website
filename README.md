# Vista Home Health Services website

A static brochure website. No backend, login, patient-data collection, forms, analytics or external scripts.

## GitHub Pages

The `gh-pages` branch contains the publishable website at its root. In repository Settings > Pages, choose Deploy from a branch, gh-pages, /(root). The main branch keeps the website under dist.

For routine content edits, edit index.html on gh-pages. Styles are in styles.css, typography.css, refinements.css and client-revisions.css; assets are in assets. Mirror approved changes into main/dist to keep the source copy current.

A public repository can use Pages on GitHub Free. Private repositories require an eligible paid GitHub plan. Review GitHub Pages terms before using it as permanent business hosting.

## Branding and photography

The logo is a cleaned rendering based on the supplied screenshot, with the date and unrelated document text removed. Replace it with the client's original vector asset when available. Illustrative stock photography does not depict Vista staff or patients.

Photo sources:
- https://www.pexels.com/photo/elderly-caregiver-shaking-hands-with-senior-woman-29372534/
- https://www.pexels.com/photo/a-man-checking-the-elderly-woman-s-blood-pressure-using-sphygmomanometer-7446763/

Lora and Source Sans 3 are locally hosted with their included SIL Open Font Licenses. The two-sided, six-panel PDF brochure is generated from the approved website copy. The original Word document is not included.

## Client handoff

Client should approve services, business contact details, hours, billing and accreditation wording. This site describes home health services. Accreditation information is attributed to the brochure and is not independently verified.

Client should own the GitHub repository and domain. Keep existing email DNS records when connecting the domain. Never commit credentials, internal documents or patient information.

## Regenerating the tri-fold brochure

From the main-branch checkout, install Python dependencies with `python3 -m pip install reportlab pillow`, then run `python3 scripts/generate_trifold.py`. This reads `dist/index.html` and writes `dist/assets/vista-brochure.pdf`. Regenerate after approved copy changes and review both rendered PDF sides before publishing the matching PDF to `gh-pages/assets/vista-brochure.pdf`.

The brochure uses US Letter landscape with a narrower fold-in flap. Confirm paper, fold direction and any bleed requirements with the printer. Brochure stock-image credits and license links are in `brochure-assets/SOURCES.md`.
