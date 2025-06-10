# Cartogram Tool

This repository contains a TopoJSON file of U.S. states (`us.json`) and a
utility script to generate contiguous cartograms from arbitrary state data.

## Requirements

```
pip install -r requirements.txt
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

A small `template.csv` file is provided as an example. Each row now includes the
state name so you can easily edit the values. Use it as a starting point for
your own data or download it directly from the web interface.

Run the script to produce a GeoJSON cartogram:

```
python3 generate_cartogram.py us.json data.csv -o output.geojson
```

The resulting `output.geojson` contains transformed geometries which can be
visualized with standard GIS tools.

## Web Application

Run a small Flask server to generate cartograms directly in the browser:

```
python3 app.py
```

Navigate to `http://localhost:5000` and upload a CSV file with `id` and `value`
columns to see the resulting cartogram rendered with D3.

The web page now provides a simple navigation menu. You can download the
`template.csv` directly from there, add short informational notes, and export
the rendered cartogram as a PNG image.  A preset drop-down lets you quickly
generate cartograms for built in datasets such as population, land area and a
synthetic GDP metric.  Clicking on a state displays a small popup with the
state name and its current value.
