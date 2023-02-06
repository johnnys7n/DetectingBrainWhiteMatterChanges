from app import app
from flask import request, render_template, session, make_response
import os
from skimage.metrics import structural_similarity
import imutils
import cv2 as cv
from PIL import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import base64
from io import BytesIO
import tempfile
from app.contours import GettingContours
from app.histogram import GetHist


# Adding path to config
app.config['UPLOADED'] = 'app/static/uploads'
app.config['GENERATED'] = 'app/static/generated'
app.config['GRAPHS'] = 'app/static/graphs'

# Route to home page


@app.route("/")
def home():
    return render_template('home.html')

# Route to contours page


@app.route("/contours", methods=["GET", "POST"])
def contours():
    if request.method == "POST":  # execute if request is post
        f = GettingContours()
        f.get_contours('file_upload1', 'file_upload2')


@app.route('/contours_show_image')
def displayImage():
    # Getting uploaded file path from session
    diff = os.path.join(app.config['GENERATED'], 'image_diff.png')
    return render_template('contours_show_image.html')

# Routes to the histogram page


@app.route('/histogram', methods=['GET', 'POST'])
def hist():
    if request.method == 'POST':  # executes when the request is post
        f = GetHist()
        f.get_histogram('file_upload')

    # Main function
if __name__ == '__main__':
    app.run(debug=True)
