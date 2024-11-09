from flask import Blueprint, render_template, request

main_blueprint = Blueprint("main", __name__)

@main_blueprint.route("/", methods=["GET"])
def index():
    # Renders the initial form page
    return render_template("index.html", prediction=None)

@main_blueprint.route("/recommendation", methods=["POST"])
def recommendation():
    # Collect form data
    username = request.form.get("username")
    api_key = request.form.get("api-key")
    genres = request.form.getlist("genre")
    feelings = request.form.getlist("feeling")

    # Simple recommendation logic based on genres and feelings
    if "pop" in genres and "joy" in feelings:
        pred_class = "Happy Pop Vibes"
    elif "classical" in genres and "calm" in feelings:
        pred_class = "Classical Serenity"
    elif "rock" in genres and "anger" in feelings:
        pred_class = "Rock Rage"
    else:
        pred_class = "Ambient Dreams"

    # Render the index.html template with the prediction result
    return render_template("index.html", prediction=pred_class)