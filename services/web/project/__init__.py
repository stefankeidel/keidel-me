import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from similarity import pairwise

ALLOWED_EXTENSIONS = set(["txt", "pdf", "doc", "docx", "odt"])
UPLOAD_FOLDER = '/home/app/web/files/'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def upload_form():
    return render_template("upload.html")


@app.route("/upload", methods=["POST"])
def upload_file():
    if request.method == "POST":
        if "files[]" not in request.files:
            flash("No file selected")
            return redirect("/")
        files = request.files.getlist("files[]")
        saved_file_list = []
        for file in files:
            if file and allowed_file(file.filename):
                file_path = os.path.join(
                    app.config["UPLOAD_FOLDER"], secure_filename(file.filename)
                )
                file.save(file_path)
                saved_file_list.append(file_path)

        if len(saved_file_list) > 0:
            similarity = pairwise(saved_file_list)
            return render_template("result.html", similarity_array=similarity)

        return redirect("/")


if __name__ == "__main__":
    app.run()
