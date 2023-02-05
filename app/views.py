# Important imports
from app import app
from flask import request, render_template, session
import os
from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np

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
            uploaded_image1 = cv2.imread(os.path.join(app.config['UPLOADED'], 'image1.png'))
            uploaded_image2 = cv2.imread(os.path.join(app.config['UPLOADED'], 'image2.png'))

            # Convert image into grayscale
            image1_gray = cv2.cvtColor(uploaded_image1, cv2.COLOR_BGR2GRAY)
            image2_gray = cv2.cvtColor(uploaded_image2, cv2.COLOR_BGR2GRAY)

            # Calculate structural similarity
            (score, diff) = structural_similarity(image1_gray, image2_gray, full=True)
            diff = (diff * 255).astype("uint8")

            # Calculate threshold and contours
            thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]
            cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            cnts = imutils.grab_contours(cnts)
            
            # Draw contours on image
            for c in cnts:
                (x, y, w, h) = cv2.boundingRect(c)
                cv2.rectangle(uploaded_image1, (x, y), (x + w, y + h), (0, 0, 255), 2)
                cv2.rectangle(uploaded_image2, (x, y), (x + w, y + h), (0, 0, 255), 2)

            # Save all output images (if required)
            cv2.imwrite(os.path.join(app.config['GENERATED'], 'image_1.png'), uploaded_image1)
            cv2.imwrite(os.path.join(app.config['GENERATED'], 'image_2.png'), uploaded_image2)
            cv2.imwrite(os.path.join(app.config['GENERATED'], 'image_diff.png'), diff)
            cv2.imwrite(os.path.join(app.config['GENERATED'], 'image_thresh.png'), thresh)
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
            uploaded_file = Image.open(file_upload).resize((250,160))
            grayed_file = cv2.cvtColor(uploaded_file, cv2.COLOR_BGR2GRAY)
            grayed_file.save(os.path.join(app.config['UPLOADED'], 'plt.png'))
            
            filename_plt = os.path.join(app.config['GENERATED'], 'plt.png')
            #reading into cv2 and converting to hist plt
            img = cv2.imread(filename_plt, 0)
            plt.hist(img.ravel(),256,[0,256])
            
            #saving histogram plot as image
            plt.savefig(os.path.join(app.config['GRAPHS'],'plt.png'))
            plot_image = os.path.join(app.config['GRAPHS'],'plt.png')

            return render_template('histogram.html', output=plot_image)
        else: #if the image is not imported and the check button is clicked
            return render_template('histogram.html', output=str('Please Input an Image'))
    else:
        return render_template('histogram.html')


# Main function
if __name__ == '__main__':
    app.run(debug=True)
