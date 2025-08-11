1. Ensure node is installed atleast version 18
2. Ensure python is installed at least version 3.9
3. Install python dependencies i.e pip install -r requirements.txt
4. cd into the backend folder and do npm install
5. run npm start and you'll see Server Started
6. run python motion-detection.py and you should see a video feed of your webcam
7. Go to http://localhost:3000
8. When motion is detected by the web cam a video will be streamed to http://localhost:3000

To test if its working make sure when the python script starts it is facing a solid background. Move infront of the camera and the video should be streamed to http://localhost:3000
Once there is no motion the last frame during motion is displayed in http://localhost:3000
