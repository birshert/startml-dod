import os

from flask import Flask, jsonify, request
from werkzeug.utils import secure_filename

from api import API_ERROR, answer_question_about_transcription, process_audio_file

UPLOAD_FOLDER = "tmp"
ALLOWED_EXTENSIONS = {"mp3", "m4a", "wav"}

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


def allowed_file(filename: str) -> bool:
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/", methods=["POST"])
def upload_file():
    file = request.files["file"]

    if file and allowed_file(file.filename):
        try:
            filename = os.path.join(app.config["UPLOAD_FOLDER"], secure_filename(file.filename))
            file.save(filename)

            result = process_audio_file(filename)

            return (
                jsonify(result),
                200,
            )
        except API_ERROR:
            return (
                jsonify({"Message": "Request to api failed"}),
                400,
            )

    return (
        jsonify({"Message": "Bad file"}),
        400,
    )


@app.route("/ask_question", methods=["POST"])
def ask_question():
    data = request.json

    transcript = data.get("transcript", "")
    question = data.get("question", "")

    try:
        answer = answer_question_about_transcription(transcript=transcript, question=question, model="gpt-4")

        return (
            jsonify({"answer": answer}),
            200,
        )
    except API_ERROR:
        return (
            jsonify({"Message": "Request to api failed"}),
            400,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=55555)
