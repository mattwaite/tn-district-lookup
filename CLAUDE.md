# CLAUDE.md

Single-page web app: readers enter a street address and learn which U.S.
House district they live in under Tennessee's redrawn 2026 congressional
maps. Built for a non-profit newsroom — zero hosting cost, no API keys,
embedded in a CMS via iframe.

Live site: https://mattwaite.github.io/tn-district-lookup/ (GitHub Pages,
served from `main` branch root — pushing to `main` deploys).

## Architecture

There is no build step, no framework, and no server. The entire app is
`index.html` (markup, CSS, and vanilla ES5 JavaScript in one file) plus
`districts.json`.

- **Geocoding**: U.S. Census Bureau geocoder via **JSONP, not fetch** —
  the geocoder does not send CORS headers, so plain fetch fails
  cross-origin. Don't "simplify" the JSONP transport away without
  re-verifying CORS support.
- **District matching**: client-side ray-casting point-in-polygon against
  `districts.json` (handles MultiPolygons and holes).
- **Map**: Leaflet from unpkg CDN with CARTO's free light basemap.
- **Iframe embedding**: pym.js child is initialized when present; call
  `tellParent()` after any UI change that alters page height.

## Data

`districts.json` is GeoJSON converted from the state's official shapefiles
in `NewCongressional26/` (WGS84, 9 districts, properties `district` and
`name`). Coordinates are rounded to 6 decimals; geometry is otherwise
full-resolution on purpose — accuracy at district boundaries matters more
than file size, and GitHub Pages gzips it to ~870KB.

To regenerate after a corrected shapefile drop:

```bash
python3 -m venv .venv && .venv/bin/pip install pyshp
.venv/bin/python convert.py
```

Note: the new map renumbers districts substantially vs. the pre-2026 map
(e.g. downtown Memphis is in District 5, not the old 9th). Surprising
lookup results are likely correct — check the shapefile before assuming a
bug.

## Local development

`fetch()` can't load `districts.json` from `file://`, so:

```bash
python3 -m http.server 8000   # then open http://localhost:8000
```

## Constraints to preserve

- Zero cost: no paid APIs, no keys, no server-side code.
- Addresses must never be stored or sent anywhere except the Census
  geocoder (the page promises this to readers).
- Keep the app dependency-light and in a single HTML file; the newsroom
  maintains this without a build toolchain.
