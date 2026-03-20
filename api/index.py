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

    try:
        response = requests.post(
            "https://api.ocr.space/parse/image",
            files={"file": (file.filename, file.stream, file.mimetype)},
            data={"apikey": API_KEY}
        )

        # 👇 IMPORTANT: print raw response
        print("RAW RESPONSE:", response.text)

        # Try JSON
        result = response.json()

    except Exception as e:
        return "Request failed: " + str(e)

    # 👇 FIX: handle if string comes
    if isinstance(result, str):
        return "API returned string: " + result

    # 👇 SAFE access
    if result.get("IsErroredOnProcessing"):
        return "API Error: " + str(result)

    try:
        return result["ParsedResults"][0]["ParsedText"]
    except Exception as e:
        return "Parsing error: " + str(result)@app.route("/", methods=["GET", "POST"])
    
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


    
