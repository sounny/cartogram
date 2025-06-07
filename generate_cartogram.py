#!/usr/bin/env python3
"""Generate a contiguous cartogram from a TopoJSON and CSV state data.

The script expects a TopoJSON file with US state geometries (such as the
`us.json` file in this repository) and a CSV file containing at least two
columns: `id` (FIPS code matching the TopoJSON `id`) and `value` which
is the numeric value used to scale states in the cartogram.

Example usage:
    python3 generate_cartogram.py us.json data.csv -o cartogram.geojson
"""
from __future__ import annotations

import argparse
import json
import sys

import geopandas as gpd
import pandas as pd
from cartogram import cartogram as cg
from topojson import Topology


def load_states(topojson_path: str) -> gpd.GeoDataFrame:
    """Load US states from a TopoJSON file as a GeoDataFrame with an `id` column."""
    with open(topojson_path) as f:
        topo_data = json.load(f)
    topo = Topology(topo_data, object_name="states")
    features = json.loads(topo.to_geojson())['features']

    for f in features:
        # Preserve the feature id so it can be merged with the CSV data
        f.setdefault('properties', {})['id'] = f['id']
    return gpd.GeoDataFrame.from_features(features)


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate contiguous cartogram")
    parser.add_argument("topojson", help="Input TopoJSON file with state shapes")
    parser.add_argument("csv", help="CSV containing columns 'id' and 'value'")
    parser.add_argument("-o", "--output", default="cartogram.geojson",
                        help="Output GeoJSON path (default: cartogram.geojson)")
    parser.add_argument("--iterations", type=int, default=5,
                        help="Number of cartogram iterations (default: 5)")
    args = parser.parse_args()

    states = load_states(args.topojson)
    data = pd.read_csv(args.csv)
    if "id" not in data.columns or "value" not in data.columns:
        sys.exit("CSV file must contain 'id' and 'value' columns")
    data["id"] = data["id"].astype(int)

    merged = states.merge(data, on="id", how="left")
    if merged["value"].isna().any():
        missing = merged[merged["value"].isna()]["id"].tolist()
        sys.exit(f"Missing value for state ids: {missing}")

    carto = cg.Cartogram(
        merged,
        "value",
        max_iterations=args.iterations,
        verbose=True,
    )
    carto.to_file(args.output, driver="GeoJSON")
    print(f"Cartogram written to {args.output}")


if __name__ == "__main__":
    main()
