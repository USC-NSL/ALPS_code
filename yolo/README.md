# Yolo
This folder contains all files you will need to train and test Yolo detector

## Requirements
- Opencv 2.x installed
- OS: Linux (Ubuntu preferred)

## Features
- Save all positive detected images into 'detect_res/'
- Writes all detection results in 'log.txt'
- Can use a folder containing images as input. The following processing is automatic.

## First of All
- Go through [this link](http://pjreddie.com/darknet/yolo/) to understand Yolo and download needed files.
- Then copy all the dirs and 'test_yolo.sh' to yolo's dir. Replace the original dir ('src/')
- In 'data/labels', create a special lable image for your object
- **'make' whole program**

## Training
- Collect your pos and neg images (size about 600x600 preferred).  
1. Make sure the images can ONLY be 'jpg' format.  
2. Space should NOT appear in the file name or in the path  
3. You can use 'train/img_trim.py' to generate lots of neg images from given image dataset. But make sure there is no positive case in theses images.
- Generate label files for pos images with tools in 'train/img_marker'. The files will be stored in 'train/img_marker/pos/' 
- Then use 'train/gen_neg_txt.sh' to create label files for neg images
- Put all image in a dir called 'JPEGImages'
- Put all label files in a dir called 'labels'
- Run 'train/gen_all_txt.sh' to generate 'train.txt' that contains all image names in 'JPEGImages'
- Change the src and backup path in 'src/yolo.c':train_yolo
- Do training!

## Testing
- Use 'test_yolo.sh'. Results will be stored in 'detect_res'
- The detection result will be logged in 'log.txt'. In the text file, the first line is image name, the second line is imgWid/imgHei/boxL/boxR/boxT/boxB;
