from flask import Flask, render_template, request, send_file
import requests
import os

app = Flask(__name__, template_folder="../templates")

OUTPUT_FILE = "output.txt"

# 🔴 For now keep API key here (simple)
API_KEY = os.environ.get("K84836366188957")

def extract_text(file):
    API_KEY = os.environ.get("OCR_API_KEY")

    if not API_KEY:
        return "API key missing"

    response = requests.post(
        "https://api.ocr.space/parse/image",
        files={"file": (file.filename, file.stream, file.mimetype)},
        data={"apikey": API_KEY}
    )

    try:
        result = response.json()
    except:
        return "Invalid response from OCR API"

    # 👇 SAFE CHECK
    if not isinstance(result, dict):
        return "Unexpected response: " + str(result)

    if result.get("IsErroredOnProcessing"):
        return "API Error: " + str(result.get("ErrorMessage"))

    try:
        return result["ParsedResults"][0]["ParsedText"]
    except:
        return "No text found"

@app.route("/", methods=["GET", "POST"])
def index():
    text = ""

    if request.method == "POST":
        file = request.files["image"]

        if file:
            # Direct file send (no saving needed)
            text = extract_text(file)

            # Save for download
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(text)

    return render_template("index.html", text=text)

@app.route("/download")
def download():
    return send_file(OUTPUT_FILE, as_attachment=True)

# ✅ Local run
if __name__ == "__main__":
    app.run(debug=True)
    
    print("API KEY:", API_KEY)
