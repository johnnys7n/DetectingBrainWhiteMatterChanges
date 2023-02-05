#White Matter Detection in the Brain

White matter is the part of the brain that is heavily enriched in myelin, a fatty substance that causes increased signal transduction across the neurons using saltatory conduction. This project is to apply computer vision OpenCV and Flask to create an application that can detect the minute contour differences in the histological and/or MRI images of the brain and displaying the image containing regional differences. 

<img src='https://www.brainline.org/sites/default/files/slides/fmri.jpg'>

###Local instructions to run the application:
####Step to run application:
* Step 1:	Create the copy of the project.
* Step 2: Open command prompt and change your current path to folder where you can find 'app.py' file.
* Step 3: Create environment by command given below:
	conda create -name <environment name>
* Step 4: Activate environment by command as follows:
	conda activate <environment name>
* Step 5: Use command below to install required dependencies:
	python -m pip install -r requirements.txt
* Step 6: Run application by command:
	**python app.py**
You will get url copy it and paste in browser.
* Step 7: Lastly Test your images.

Currently Working on:
* Outputing the regional anatomical areas of the brain and its specific structural similarity score (ie. Thalamus, Hippocampus, Corpus Callosum, Cortex, etc)
