from flask import Flask, render_template, request, redirect, url_for, flash, send_from_directory
import replicate
import os

app = Flask(__name__)
app.secret_key = 'supersecretkeyeysupersupersecret'  # This is for flashing messages
app.config['UPLOAD_FOLDER'] = 'uploads'

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        image = request.files['wound_image']
        if image:
            image_path = os.path.join(app.config['UPLOAD_FOLDER'], image.filename)
            image.save(image_path)
            result = classify_wound(image_path)
            flash(result)
            return render_template('index.html', uploaded_image=image.filename)
    return render_template('index.html', uploaded_image=None)

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

def classify_wound(image_path):
    # Set API token
    os.environ["REPLICATE_API_TOKEN"] = "ce0ec1aef6cec8114118bd0424aa8f95f5d1ee5b"

    # Call the API
    prompt = """
    Bitte klassifiziere das bereitgestellte Foto basierend auf der Widmer-Einteilung zur chronischen venösen Insuffizienz (mod. nach Marshall). Identifiziere den Grad der Wunde gemäß den folgenden Kriterien:

    • Grad 1: Corona phlebectatica paraplantaris (lokale Gefäßerweiterungen am medialen und lateralen Fußrand), Phlebödem.
    • Grad 2: Zusätzlich zu Grad 1, trophische Störungen mit Ausnahme des Ulcus cruris, wie Dermatoliposklerose, Pigmentveränderungen (Purpura jaune d’ocre), Atrophie blanche, Stauungsekzem.
    • Grad 3: Ulcus cruris venosum.
    • Grad 3a: Abgeheiltes Ulcus cruris venosum.
    • Grad 3b: Florides Ulcus cruris venosum.

    Bitte antworte AUSSCHLIESSLICH mit der Kategorie zum Beispiel "Grad 1: Corona phlebectatica paraplantaris (lokale Gefäßerweiterungen am medialen und lateralen Fußrand), Phlebödem." oder "nicht zutreffend". Kein anderer oder weiterer Text!
    """
    output = replicate.run(
        "yorickvp/llava-13b:2facb4a474a0462c15041b78b1ad70952ea46b5ec6ad29583c0b29dbd4249591",
        input={"image": open(image_path, "rb"), "prompt": prompt, "temperature": 0.1, "top_p": 0.1, "max_tokens": 100}
    )

    response = "".join(list(output))
    return response

if __name__ == '__main__':
    app.run(debug=True)
