# Cartogram Tool

This repository contains a TopoJSON file of U.S. states (`us.json`) and a
utility script to generate contiguous cartograms from arbitrary state data.

## Requirements

```
pip install cartogram geopandas topojson pandas
```

## Usage

Prepare a CSV file with FIPS codes and a numeric value for each state. The CSV
must contain at least two columns named `id` and `value`:

```
id,value
1,10.2
2,5.4
...
```

Run the script to produce a GeoJSON cartogram:

```
python3 generate_cartogram.py us.json data.csv -o output.geojson
```

The resulting `output.geojson` contains transformed geometries which can be
visualized with standard GIS tools.
