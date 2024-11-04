from flask import Flask, request, render_template
from pickle import load
import regex as re
import os
from nltk import download
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

#website link https://ml-web-app-using-flask-e8bg.onrender.com/


# Define the Flask app and set the template folder path
app = Flask(__name__, template_folder='../templates')

#class_dict = {
   # "1": "POSITIVE",
   # "0": "NEGATIVE"
#}

# Ensure wordnet and stopwords are downloaded once
download("wordnet")
download("stopwords")
stop_words = stopwords.words("english")
lemmatizer = WordNetLemmatizer()

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        # Handle form submission
        val1 = str(request.form["val1"])

        # Make a prediction using the SVM model
        pred_class = val1
    else:
        # Handle initial GET request
        pred_class = None

    # Render the template with the prediction result (or None if GET request)
    return render_template("index.html", prediction=pred_class)

@app.route("/recommendation", methods=["POST"])
def recommendation():
    # Get the input value
    val1 = str(request.form["val1"])

    # Use the input value as the prediction or make a prediction using a model if available
    pred_class = val1  # Replace with model prediction logic if needed

    # Render a new page with the prediction result
    return render_template("recommendation.html", prediction=pred_class)



if __name__ == "__main__":
    # Use the port provided by Render, or default to 5000
    port = int(os.environ.get("PORT", 5000))
    # Set host to 0.0.0.0 to be accessible externally
    app.run(host="0.0.0.0", port=port, debug=True)