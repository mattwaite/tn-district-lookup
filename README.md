# Tennessee Congressional District Lookup

A single-page app that lets readers type their address and find out which
U.S. House district they live in under Tennessee's redrawn 2026 congressional
maps. Built for free hosting on GitHub Pages and embedding in a CMS via iframe.

## How it works (all free, no API keys)

- **Geocoding** — the address is sent to the [U.S. Census Bureau geocoder](https://geocoding.geo.census.gov/),
  which is free, requires no key, and has no practical rate limits for this use.
  Addresses are never stored.
- **District matching** — happens entirely in the reader's browser with a
  point-in-polygon test against `districts.json` (converted at full resolution
  from the state's official shapefiles).
- **Map** — [Leaflet](https://leafletjs.com/) with CARTO's free light basemap.

## Files

| File | Purpose |
|---|---|
| `index.html` | The entire app (markup, styles, and JavaScript) |
| `districts.json` | District boundaries as GeoJSON, converted from `NewCongressional26/` |
| `NewCongressional26/` | Original state shapefiles (not needed for deployment) |

## Deploying to GitHub Pages

1. Create a new GitHub repository and push `index.html` and `districts.json`
   (the shapefile folder is optional but nice for transparency).
2. In the repo: **Settings → Pages → Source: Deploy from a branch**, pick
   `main` and `/ (root)`.
3. The app will be live at `https://<your-org>.github.io/<repo-name>/`.

## Embedding in your CMS

Basic iframe:

```html
<iframe src="https://<your-org>.github.io/<repo-name>/"
        width="100%" height="950" frameborder="0"
        title="Find your new Tennessee congressional district"></iframe>
```

The page also includes [pym.js](https://blog.apps.npr.org/pym.js/) child
support, so if your CMS embed uses pym the iframe will resize automatically:

```html
<div id="district-lookup"></div>
<script src="https://pym.nprapps.org/pym.v1.min.js"></script>
<script>new pym.Parent("district-lookup", "https://<your-org>.github.io/<repo-name>/");</script>
```

## Regenerating districts.json

If the state issues corrected shapefiles, drop them in and rerun:

```bash
python3 -m venv .venv && .venv/bin/pip install pyshp
.venv/bin/python convert.py
```

## Testing locally

`fetch()` won't load `districts.json` from `file://`, so run a local server:

```bash
python3 -m http.server 8000
# open http://localhost:8000
```
