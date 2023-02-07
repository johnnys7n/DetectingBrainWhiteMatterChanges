# setting output to null for jinja frontend
class GetHist():
    def __init__(self, image1):
        self.image1 = image1

    def get_histogram(self):
        output = False

        file_upload = request.files[self.image1]
        filename = file_upload.filename

        # if the image is imported
        if file_upload:
            # uploading and saving file:
            uploaded_file = Image.open(file_upload)
            uploaded_file.save(os.path.join(app.config['UPLOADED'], 'plt.png'))

            # change to numpy array
            img1 = cv.imread(os.path.join(app.config['UPLOADED'], 'plt.png'))

            # reading into cv and converting to hist plt
            hist = cv.calcHist([img1], [0], None, [256], [0, 256])

            # creating a graph of the histogram output
            fig = Figure()
            canvas = FigureCanvas(fig)
            axes = fig.add_subplot()
            axes.set_title(f'Histogram for Pixel Intensity: {filename}')
            axes.set_ylabel('No of Pixels')
            axes.set_xlabel('Pixel Values')

            # plot the data
            axes.plot(hist)

            # saving plotted image into a new folder as png then decoding
            buf = BytesIO()
            fig.savefig(buf, format='png')
            data = base64.b64encode(buf.getbuffer())
            img_plt = Image.open(BytesIO(base64.b64decode(data)))
            img_plt.save(os.path.join(app.config['GRAPHS'], 'plt_pic.png'))
            return render_template('histogram.html', output=True)
        else:  # if the image is not imported and the check button is clicked
            return render_template('histogram.html', output=str('Please Input an Image'))
    else:
        return render_template('histogram.html')
