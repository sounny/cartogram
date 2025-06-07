# Cartogram Tool

This repository contains a TopoJSON file of U.S. states (`us.json`) and a
utility script to generate contiguous cartograms from arbitrary state data.

## Requirements

```
pip install cartogram geopandas topojson pandas Flask
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

## Web Application

A simple Flask app is included to run the cartogram generator via your browser.

Start the server:

```
python3 app.py
```

Open [http://localhost:5000](http://localhost:5000) and upload a CSV file with
`id` and `value` columns. The generated GeoJSON will be downloaded
automatically.
