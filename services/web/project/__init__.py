import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
from similarity import pairwise


app = Flask(__name__)
app.config.from_object("project.config.Config")
app.secret_key = os.getenv("FLASK_SECRET_KEY")


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in set(
        ["txt", "pdf", "doc", "docx", "odt"]
    )


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
        file_name_list = []
        for file in files:
            if file and allowed_file(file.filename):
                file_path = os.path.join(
                    app.config["UPLOAD_FOLDER"], secure_filename(file.filename)
                )
                file.save(file_path)
                saved_file_list.append(file_path)
                file_name_list.append(secure_filename(file.filename))

        if len(saved_file_list) > 0:
            similarity = pairwise(saved_file_list, round_decimals=2)
            return render_template(
                "result.html",
                similarity_array=similarity,
                file_name_list=file_name_list,
            )

        return redirect("/")


if __name__ == "__main__":
    app.run()
