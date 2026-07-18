# 🎨 CV visual identity

The CV uses one restrained, recruiter-first visual system across English,
Spanish and Hebrew.

- `cv-banner.svg` — static, accessible banner shared by the repository README
  and all three CV documents.
- `social/cv-social-preview.svg` — editable 1280 × 640 source for the
  repository social card.
- `social/cv-social-preview.png` — upload-ready 1280 × 640 PNG generated from
  the SVG source.

The visuals contain only public, verified identity and positioning. They use no
external fonts, scripts, animation, tracking or remotely hosted assets.

To rebuild the PNG on Windows with Microsoft Edge installed:

```powershell
powershell -ExecutionPolicy Bypass -File tools/render_cv_social_preview.ps1
```

After rendering, run `python tools/verify_cv.py`. Uploading the PNG through
GitHub repository settings is a separate public action and is never automatic.
