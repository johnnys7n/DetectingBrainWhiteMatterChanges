# Important imports
from app import app
from flask import request, render_template, session
import os
from skimage.metrics import structural_similarity
import imutils
import cv2
from PIL import Image

# Adding path to config
app.config['UPLOADED'] = 'app/static/uploads'
app.config['GENERATED'] = 'app/static/generated'

# Route to home page
@app.route("/", methods=["GET", "POST"])
def index():

	# Execute if request is get
	if request.method == "GET":
	    return render_template("index.html")

	# Execute if request is post
	if request.method == "POST":
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
                    return render_template('index.html',pred=str(round(score*100,2)) + '%' + ' correct')
                else:
                    return render_template('index.html',pred=str('Please Input Both Images'))
@app.route('/show_image')
def displayImage():
    # Getting uploaded file path from session
    diff = os.path.join(app.config['GENERATED'], 'image_diff.png')
    return render_template('index3.html')

# Main function
if __name__ == '__main__':
    app.run(debug=True)
