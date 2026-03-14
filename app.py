from __future__ import annotations

import os
import tempfile

from flask import Flask, request, Response

from generate_cartogram import generate_cartogram_df

app = Flask(__name__, static_folder=".", static_url_path="")


@app.route("/")
def index() -> Response:
    return app.send_static_file("index.html")


@app.route("/cartogram", methods=["POST"])
def cartogram_route() -> Response:
    if "file" not in request.files:
        return Response("Missing CSV file", status=400)

    iterations_raw = request.form.get("iterations", "5")
    try:
        iterations = int(iterations_raw)
    except (TypeError, ValueError):
        return Response("Iterations must be an integer", status=400)

    if iterations < 1 or iterations > 25:
        return Response("Iterations must be between 1 and 25", status=400)

    file = request.files["file"]
    with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
        file.save(tmp.name)
        tmp_path = tmp.name
    try:
        carto = generate_cartogram_df("us.json", tmp_path, iterations)
        geojson = carto.to_json()
    except Exception as exc:
        return Response(str(exc), status=400)
    finally:
        os.remove(tmp_path)
    return Response(geojson, content_type="application/json")


if __name__ == "__main__":
    app.run(debug=True)
