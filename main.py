from flask import Flask, render_template, request, send_file
from parser import parse_log
from io import BytesIO
import json

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():
    result = []

    if request.method == "POST":
        log_data = ""

        # Check for pasted log
        if "log" in request.form and request.form["log"].strip():
            log_data = request.form["log"]

        # Check for uploaded file
        elif "logfile" in request.files:
            uploaded_file = request.files["logfile"]
            if uploaded_file and uploaded_file.filename:
                try:
                    log_data = uploaded_file.read().decode("utf-8")
                except Exception as e:
                    result.append({"error": f"Failed to read file: {str(e)}"})

        # Parse log lines
        if log_data:
            logs = log_data.strip().splitlines()
            for line in logs:
                try:
                    parsed = parse_log(line)
                    result.append(parsed)
                except Exception as e:
                    result.append({"error": f"Invalid log line: '{line}' - {str(e)}"})

    return render_template("index.html", result=result)

@app.route("/download", methods=["POST"])
def download():
    data = request.form.get("data")
    if not data:
        return "No data to download", 400

    try:
        json_data = json.dumps(json.loads(data), indent=4)
    except json.JSONDecodeError:
        return "Invalid data format", 400

    buffer = BytesIO()
    buffer.write(json_data.encode())
    buffer.seek(0)
    return send_file(buffer, as_attachment=True, download_name="parsed_logs.json", mimetype="application/json")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)