Face Recognition using Coral USB Accelerator, Flask and Socketio

Prerequisite: 
- You need to setup Coral USB accelerator on your computer by installing tflite-runtime, pycoral and edgetpu-runtime. Follow this link for tutorial https://coral.ai/docs/accelerator/get-started/
- You need a trained edgetpu model(.tflite) and a label(.txt) file. You can use this tutorial https://coral.ai/docs/edgetpu/retrain-classification-ondevice/
- This uses pretrained haarcascade from opencv to detect face. Download it from https://github.com/opencv/opencv/tree/master/data/haarcascades

Dependencies:
- Pycoral
- tflite-runtime==2.5.0
- Flask
- Flask-socketio
- PIL
- Numpy
- OpenCV


faceext.py is a helper script you can use to extract face from images for further training.

Usage:

- python server.py --model *path_to_model* --labels *path_to_label_file* --haar *path_to_haar_cascade*
- For faceext, python faceext.py --get *path_of_folder_to_source_images* --save *path_to_location_to_save*