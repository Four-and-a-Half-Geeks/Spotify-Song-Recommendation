from flask import Flask, request, render_template
import os

app = Flask(__name__, template_folder='../templates')

@app.route("/", methods=["GET"])
def index():
    # Renders the initial form page
    return render_template("index.html", prediction=None)

@app.route("/recommendation", methods=["POST"])
def recommendation():
    # Collect form data
    username = request.form.get("username")
    api_key = request.form.get("api-key")
    genres = request.form.getlist("genre")
    feelings = request.form.getlist("feeling")

    # Simple recommendation logic based on genres and feelings (replace with real model if available)
    if "pop" in genres and "joy" in feelings:
        pred_class = "Happy Pop Vibes"
    elif "classical" in genres and "calmness" in feelings:
        pred_class = "Classical Serenity"
    elif "rock" in genres and "anger" in feelings:
        pred_class = "Rock Rage"
    else:
        pred_class = "Ambient Dreams"

    # Render the index.html template with the prediction result
    return render_template("index.html", prediction=pred_class)

if __name__ == "__main__":
    # Use the port provided by Render, or default to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)