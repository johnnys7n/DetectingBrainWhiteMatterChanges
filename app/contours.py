from flask import request, render_template, session, make_response
from flask import request, render_template, session, make_response
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
from app import app


app.config['UPLOADED'] = 'app/static/uploads'
app.config['GENERATED'] = 'app/static/generated'
app.config['GRAPHS'] = 'app/static/graphs'


class GettingContours():
    def __init__(self, img1=None, img2=None):
        self.image1 = img1
        self.image2 = img2

    def get_contours(self):
        # Get uploaded image
        file_upload1 = request.files[self.image1]
        filename1 = file_upload1.filename

        file_upload2 = request.files[self.image2]
        filename2 = file_upload1.filename

        if file_upload2 and file_upload1:
            # Resize and save the uploaded image
            uploaded_image1 = Image.open(file_upload1).resize((250, 160))
            uploaded_image1.save(os.path.join(
                app.config['UPLOADED'], 'image1.png'))
            uploaded_image2 = Image.open(file_upload2).resize((250, 160))
            uploaded_image2.save(os.path.join(
                app.config['UPLOADED'], 'image2.png'))

            # Read uploaded and original image as array
            uploaded_image1 = cv.imread(os.path.join(
                app.config['UPLOADED'], 'image1.png'))
            uploaded_image2 = cv.imread(os.path.join(
                app.config['UPLOADED'], 'image2.png'))

            # Convert image into grayscale
            image1_gray = cv.cvtColor(uploaded_image1, cv.COLOR_BGR2GRAY)
            image2_gray = cv.cvtColor(uploaded_image2, cv.COLOR_BGR2GRAY)

            # Calculate structural similarity
            (score, diff) = structural_similarity(
                image1_gray, image2_gray, full=True)
            diff = (diff * 255).astype("uint8")

            # Calculate threshold and contours
            thresh = cv.threshold(
                diff, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
            cnts = cv.findContours(
                thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)

            # Draw contours on image
            for c in cnts:
                (x, y, w, h) = cv.boundingRect(c)
                cv.rectangle(uploaded_image1, (x, y),
                             (x + w, y + h), (0, 0, 255), 2)
                cv.rectangle(uploaded_image2, (x, y),
                             (x + w, y + h), (0, 0, 255), 2)

            # Save all output images (if requestuired)
            cv.imwrite(os.path.join(
                app.config['GENERATED'], 'image_1.png'), uploaded_image1)
            cv.imwrite(os.path.join(
                app.config['GENERATED'], 'image_2.png'), uploaded_image2)
            cv.imwrite(os.path.join(
                app.config['GENERATED'], 'image_diff.png'), diff)
            cv.imwrite(os.path.join(
                app.config['GENERATED'], 'image_thresh.png'), thresh)
            return render_template('contours.html', pred='Structural Similarity: ' + str(round(score*100, 2)) + '%')

        else:
            return render_template('contours.html', pred=str('Please Input Both Images'))
