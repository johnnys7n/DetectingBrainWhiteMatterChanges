# Important imports
from app import app
from flask import request, render_template, session
import os
from skimage.metrics import structural_similarity
import imutils
import cv2 as cv
from PIL import Image
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import base64
import io

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
    if request.method == "POST": #execute if request is post
        # Get uploaded image
        file_upload1 = request.files['file_upload1']
        filename1 = file_upload1.filename

        file_upload2 = request.files['file_upload2']
        filename2 = file_upload1.filename

        if file_upload2 and file_upload1:
            # Resize and save the uploaded image
            uploaded_image1 = Image.open(file_upload1).resize((250,160))
            uploaded_image1.save(os.path.join(app.config['UPLOADED'], 'image1.png'))
            uploaded_image2 = Image.open(file_upload2).resize((250,160))
            uploaded_image2.save(os.path.join(app.config['UPLOADED'], 'image2.png'))

            # Read uploaded and original image as array
            uploaded_image1 = cv.imread(os.path.join(app.config['UPLOADED'], 'image1.png'))
            uploaded_image2 = cv.imread(os.path.join(app.config['UPLOADED'], 'image2.png'))

            # Convert image into grayscale
            image1_gray = cv.cvtColor(uploaded_image1, cv.COLOR_BGR2GRAY)
            image2_gray = cv.cvtColor(uploaded_image2, cv.COLOR_BGR2GRAY)

            # Calculate structural similarity
            (score, diff) = structural_similarity(image1_gray, image2_gray, full=True)
            diff = (diff * 255).astype("uint8")

            # Calculate threshold and contours
            thresh = cv.threshold(diff, 0, 255, cv.THRESH_BINARY_INV | cv.THRESH_OTSU)[1]
            cnts = cv.findContours(thresh.copy(), cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            
            # Draw contours on image
            for c in cnts:
                (x, y, w, h) = cv.boundingRect(c)
                cv.rectangle(uploaded_image1, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv.rectangle(uploaded_image2, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Save all output images (if required)
            cv.imwrite(os.path.join(app.config['GENERATED'], 'image_1.png'), uploaded_image1)
            cv.imwrite(os.path.join(app.config['GENERATED'], 'image_2.png'), uploaded_image2)
            cv.imwrite(os.path.join(app.config['GENERATED'], 'image_diff.png'), diff)
            cv.imwrite(os.path.join(app.config['GENERATED'], 'image_thresh.png'), thresh)
            return render_template('contours.html',pred='Structural Similarity: ' + str(round(score*100,2)) + '%')
        
        else:
            return render_template('contours.html',pred=str('Please Input Both Images'))
    else:
        return render_template('contours.html')

#route to the image output of the contours
@app.route('/contours_show_image')
def displayImage():
    # Getting uploaded file path from session
    diff = os.path.join(app.config['GENERATED'], 'image_diff.png')
    return render_template('contours_show_image.html')

#Routes to the histogram page
@app.route('/histogram', methods=['GET','POST'])
def hist():
    if request.method=='POST': #executes when the request is post
        file_upload = request.files['file_upload']
        filename = file_upload.filename

        #if the image is imported
        if file_upload:
            #uploading and saving file:
            uploaded_file = Image.open(file_upload)
            uploaded_file.save(os.path.join(app.config['UPLOADED'], 'plt.png'))

            #change to numpy array
            img = cv.imread(os.path.join(app.config['UPLOADED'], 'plt.png'))
            img_gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
            #reading into cv and converting to hist plt
            hist = cv.calcHist([img_gray],[0],None,[256],[0,256])
            plt.plot(hist)
            # passing images to html using base64
            img = io.BytesIO()
            plt.savefig(img, format='png')
            img.seek(0)
            figdata_png = base64.b64encode(img.getvalue())
            
            return render_template('histogram.html', output=figdata_png.decode('utf8'))
        else: #if the image is not imported and the check button is clicked
            return render_template('histogram.html', output=str('Please Input an Image'))
    else:
        return render_template('histogram.html')


# Main function
if __name__ == '__main__':
    app.run(debug=True)
