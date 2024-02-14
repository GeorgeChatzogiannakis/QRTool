# QRTool

This tool allows Reading and Writing QR codes, from, and to files, through an easy-to-use interface powered by python's tkinter library. There are three different main tabs labelled "Read", "Write" and "Webcam", each of them indicating different functionality or input methods.

### Read
+ The Read section is designed to work with image files that contain QR codes. Using the "Browse" button, navigate to a supported image type and click "Open".
+ After the file is loaded, a preview of the image will be displayed in the space between the selected file's name and the "Browse" button.
+ Once the image is loaded, the previously grey-ed out "Extract" button will become available and clicking it will display the extracted data from the QR code on a textbox, right underneath.
  An option to clear the text containing the extracted data from the textbox is also given, by clicking the "Clear" button, right under the textbox.

### Write
The "Write" tab, right next to the "Read" tab, contains the functionality that generates QR codes, containing the data passed inside the textbox. 
Once the desired information is typed in the textbox, the "Save As" button, under it, will offer you four different picture file formats to save the newly created image. 
Just navigate the directory where you want to save the QR, enter a filename and click "Save".

### Webcam
The "Webcam" tab can recognize QR codes that are shown in the camera. Just ensure that access to your webcam is available and click on the "Open Webcam" button in the middle of the window.
It will probably take a few seconds until the camera opens, and when it does, you will be able to show a QR code in your webcam in real time, and it will display the extracted information on top of the live feed, as soon as the lighting conditions are good enough for it to detect it.
+ If the QR code shown in the webcam is a URL (starting with "http" or "https"), a popup window will appear asking you if you want to follow the link in a tab inside your web browser.
  If you choose to continue, your webcam will be closed, and if you do not, the stream will continue. If access to your webcam is for any reason unsuccessful, you will be presented an error message reminding you to unblock access to your webcam, and a "Retry" button will replace the "Open Webcam".

### Thanks a lot to @CyberShadow7 for giving me the idea of creating such an app and suggesting functionalinty.
