"""Convert the state's congressional district shapefile to compact GeoJSON.

Usage: .venv/bin/python convert.py
Reads NewCongressional26/NewCongressional26.shp (WGS84) and writes
districts.json with coordinates rounded to 6 decimal places (~10 cm).
"""

import json

import shapefile

SHAPEFILE = "NewCongressional26/NewCongressional26"
OUTPUT = "districts.json"


def rnd(coords):
    if isinstance(coords[0], (int, float)):
        return [round(coords[0], 6), round(coords[1], 6)]
    return [rnd(c) for c in coords]


def main():
    reader = shapefile.Reader(SHAPEFILE)
    features = []
    for sr in reader.shapeRecords():
        geom = sr.shape.__geo_interface__
        features.append({
            "type": "Feature",
            "properties": {
                "district": sr.record["DISTRICT"],
                "name": sr.record["LONGNAME"],
            },
            "geometry": {
                "type": geom["type"],
                "coordinates": rnd(geom["coordinates"]),
            },
        })

    with open(OUTPUT, "w") as f:
        json.dump({"type": "FeatureCollection", "features": features}, f,
                  separators=(",", ":"))
    print(f"Wrote {OUTPUT} with {len(features)} districts")


if __name__ == "__main__":
    main()
