from app import app
from app.contours import GettingContours
from app.histogram import GetHist
from flask import Flask, render_template, session, make_response, request
import os
import imutils
from skimage.metrics import structural_similarity
import cv2 as cv
from PIL import Image
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import base64
from io import BytesIO
import tempfile

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
    if request.method == "POST":  # execute if req is post
        f = GettingContours('file_upload1', 'file_upload2')
        f.get_contours()
    else:
        return render_template('contours.html')


@app.route('/contours_show_image')
def displayImage():
    # Getting uploaded file path from session
    diff = os.path.join(app.config['GENERATED'], 'image_diff.png')
    return render_template('contours_show_image.html')

# Routes to the histogram page


@app.route('/histogram', methods=['GET', 'POST'])
def hist():
    if request.method == 'POST':  # executes when the req is post
        f = GetHist('file_upload')
        f.get_histogram()
    else:
        return render_template('histogram.html')

    # Main function
if __name__ == '__main__':
    app.run(debug=True)
