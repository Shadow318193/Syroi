from flask import Flask, render_template, request, redirect
from data import image_processing
from os import walk

app = Flask(__name__)


app.config["SECRET_KEY"] = "secret_key"
app.config["UPLOAD_FOLDER"] = "static/media/from_users"
app.config["MAX_CONTENT_LENGTH"] = 32 * 1024 * 1024


@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "GET":
        images = []
        for files in walk("static/media/from_users/"):
            for file in files[2]:
                if file != ".gitignore":
                    images.append((file, "".join(file.split(".")[:-1]) + "_" + file.split(".")[-1] + ".png"))
        return render_template("index.html", images=images)
    elif request.method == "POST":
        files = request.files.getlist("files[]")
        for file in files:
            filename_in = "static/media/from_users/" + file.filename
            filename_out = "static/media/rendered/" + "".join(file.filename.split(".")[:-1]) + "_" + \
                file.filename.split(".")[-1] + ".png"
            print("Вход:", filename_in)
            print("Выход:", filename_out)
            file.save(filename_in)
            if "upload" in request.form:
                chunk = request.form.get("chunk")
                rows = request.form.get("rows")
                offset = request.form.get("offset")
                image_processing.make_raw_image_mode_simple(filename_in, filename_out,
                                                            int(chunk) if chunk else image_processing.CHUNK_DEFAULT,
                                                            int(rows) if rows else image_processing.ROWS_DEFAULT,
                                                            int(offset) if offset else image_processing.OFFSET_DEFAULT)
            elif "upload_nes" in request.form:
                rows = request.form.get("rows")
                print(rows)
                color1 = tuple([int(_, 16) for _ in [request.form.get("color1")[0:2],
                                                     request.form.get("color1")[2:4],
                                                     request.form.get("color1")[4:6]]]) if \
                    request.form.get("color1") else image_processing.COLORS_FOR_NES_DEFAULT[0]
                color2 = tuple([int(_, 16) for _ in [request.form.get("color2")[0:2],
                                                     request.form.get("color2")[2:4],
                                                     request.form.get("color2")[4:6]]]) if \
                    request.form.get("color2") else image_processing.COLORS_FOR_NES_DEFAULT[1]
                color3 = tuple([int(_, 16) for _ in [request.form.get("color3")[0:2],
                                                     request.form.get("color3")[2:4],
                                                     request.form.get("color3")[4:6]]]) if \
                    request.form.get("color3") else image_processing.COLORS_FOR_NES_DEFAULT[2]
                color4 = tuple([int(_, 16) for _ in [request.form.get("color4")[0:2],
                                                     request.form.get("color4")[2:4],
                                                     request.form.get("color4")[4:6]]]) if \
                    request.form.get("color4") else image_processing.COLORS_FOR_NES_DEFAULT[3]
                image_processing.make_raw_image_mode_nes(filename_in, filename_out,
                                                         int(rows) if rows else image_processing.NES_ROWS_DEFAULT,
                                                         (color1, color2, color3, color4))
        return redirect("/")


if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)
