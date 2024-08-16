import PIL
from flask import Flask, render_template, request
from colorthief import ColorThief
import webcolors
import pybase64

app = Flask(__name__)


def get_palette(url, number, path):
    new_file = f"static/images/test.{path}"
    # check for file error
    if new_file.split('/')[-1] == 'test.':
        colors_dict = 'Error'
        return colors_dict
    else:
        with open(new_file, mode="wb") as f:
            decoded_data = pybase64.b64decode(url)
            f.write(decoded_data)
    # get color palette
        try:
            ct = ColorThief(new_file)
        except PIL.UnidentifiedImageError:
            colors_dict = 'Error'
            return colors_dict

        colors = ct.get_palette(color_count=number, quality=1)

    # get hex codes for color palette
        hex_codes = []
        for c in colors:
            hex_color = webcolors.rgb_to_hex(c)
            hex_codes.append(hex_color)

        colors_dict = {str(colors[i]): str(hex_codes[i]) for i in range(len(colors))}
        return colors_dict


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == 'POST':
        url = request.form.get("url").split(";base64,")[-1]
        number = int(request.form.get("number"))
        if request.form.get("path") == 'static/images/test.':
            error = 'Error, file not recognised. Please refresh the page and try again'
            return render_template("index.html", error=error)
        else:
            path = request.form.get("path").split(".")[-1]

        colors_dict = get_palette(url, number, path)

        if colors_dict == 'Error':
            error = 'Error, file not recognised. Please refresh the page and try again'
            return render_template("index.html", error=error)

        return render_template("index.html", colors=colors_dict, path=path)

    return render_template("index.html")


if __name__ == '__main__':
    app.run(debug=True)


