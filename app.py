from __future__ import annotations

import tempfile

from flask import Flask, request, send_file

from generate_cartogram import generate_cartogram

app = Flask(__name__)

HTML_FORM = """
<!doctype html>
<title>Cartogram Generator</title>
<h1>Upload CSV Data</h1>
<form method="post" enctype="multipart/form-data">
  <input type="file" name="csv" accept="text/csv" required><br>
  Iterations: <input type="number" name="iterations" value="5" min="1"><br>
  <input type="submit" value="Generate">
</form>
"""


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        file = request.files.get("csv")
        if not file:
            return HTML_FORM, 400
        with tempfile.NamedTemporaryFile(suffix=".csv") as csv_tmp, tempfile.NamedTemporaryFile(suffix=".geojson", delete=False) as out_tmp:
            file.save(csv_tmp.name)
            iterations = int(request.form.get("iterations", 5))
            generate_cartogram("us.json", csv_tmp.name, out_tmp.name, iterations)
            return send_file(out_tmp.name, as_attachment=True, download_name="cartogram.geojson")
    return HTML_FORM


if __name__ == "__main__":
    app.run(debug=True)
