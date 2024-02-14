import os
import cv2
import qrcode
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from PIL import ImageTk, Image
import webbrowser
import threading
import numpy as np
from pyzbar.pyzbar import decode

class QRAnalyzer:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("QR Tool")
        self.root.iconbitmap("")
        self.root.geometry("680x460")
        self.m = ttk.Notebook()

        self.Reader = ttk.Frame(self.m)
        self.Writer = ttk.Frame(self.m)
        self.Webcam = ttk.Frame(self.m)
        self.modes()

    def modes(self):
        self.m.add(self.Reader,text="Reader")
        self.m.add(self.Writer,text="Writer")
        self.m.add(self.Webcam,text="Webcam")
        self.m.pack()
        
        # region - Read
        self.PreviewFrame = tk.Frame(self.Reader)
        self.PreviewFrame.pack()

        self.directory_path_label = tk.Label(self.PreviewFrame,text="Please browse to a file")
        self.directory_path_label.pack(side=tk.LEFT)

        self.PreviewQR = tk.Label(self.Reader)
        # placeholder = Image.open("C:\\Users\George\Desktop\PROJECTS\QRImgScanner\placeholder.png")
        # ph = ImageTk.PhotoImage(placeholder)
        # self.PreviewQR.config(image=ph)
        # self.PreviewQR.image = ph
        self.PreviewQR.pack()

        btnFrame = tk.Frame(self.Reader)
        btnFrame.pack()

        self.browse_qr = tk.Button(btnFrame, text= "Browse", command=self.browse_qr)
        self.browse_qr.pack(side="left")

        self.extract_button = tk.Button(btnFrame, text= "Extract", command=self.extract_button)
        self.extract_button.pack(side="left")
        self.extract_button.config(state=tk.DISABLED)

        self.infoFrame = tk.Frame(self.Reader)
        self.infoFrame.pack_forget()

        ResultLbl = tk.Label(self.infoFrame)
        ResultLbl.config(text="Result:")
        ResultLbl.pack()

        self.QRInfo = tk.Text(self.infoFrame, width=70, height=11)
        self.QRInfo.pack(side="top")

        self.clear_button = tk.Button(self.infoFrame,text="Clear", command=self.clearTextbox)
        self.clear_button.pack_forget()
        # endregion - Read

        # region - Write
        CreateQrFrame = tk.Frame(self.Writer)
        CreateQrFrame.pack()

        CreateQrLabel = tk.Label(self.Writer, text="Create QR")
        CreateQrLabel.pack()

        self.TextboxFrame = tk.Frame(self.Writer)
        self.TextboxFrame.pack()
        self.data = tk.Text(self.TextboxFrame,width=50, height=18)
        self.data.pack()

        self.save_btn = tk.Button(self.Writer,text="Save As",command=self.saveQr)
        self.save_btn.pack(pady=15)
        # endregion

        # region webcam
        def is_valid_url(url):
            # You may need to use a more sophisticated URL validation approach
            # This simple check assumes that any string starting with "http://" or "https://" is a URL
            return url.startswith("http://") or url.startswith("https://")
        camIsOpen = False
        self.url_opened = False
        WebCamFrame = tk.Frame(self.Webcam)
        WebCamFrame.pack()

        CameraMsg = tk.Label(WebCamFrame,text="Initiating Webcam \n Please Wait")

        def hideMsg():
            CameraMsg.pack_forget()

        def openWebCam():
            nonlocal camIsOpen
            global Camera2
            if not camIsOpen:
                self.webcamThread = threading.Thread(target=openCam)
                self.webcamThread.daemon = True
                self.webcamThread.start()
                camIsOpen = True
                CameraMsg.pack()
                self.root.after(9000,hideMsg)
            Camera.pack_forget()
            Camera2 = tk.Button(WebCamFrame, text="Close Webcam Stream", command=closeWebcam)
                    
        def closeWebcam():
            nonlocal camIsOpen
            if camIsOpen:
                try:
                    camIsOpen = False
                    Camera2.pack_forget()
                    hideMsg()
                except RuntimeError as e:
                    messagebox.showerror("Runtime Error",e)
            else:
                Camera2.pack_forget()

        def openCam():
            nonlocal camIsOpen
            cam = cv2.VideoCapture(0)
            cam.set(3, 426)
            cam.set(4, 240)
            camIsOpen = True

            label = tk.Label(WebCamFrame)
            label.pack()

            while camIsOpen:
                successful, img = cam.read()

                if not successful:
                    def retried():
                        Camera2.pack_forget()
                        retry_btn.pack_forget()
                        hideMsg()
                        closeWebcam()
                        openWebCam()
                        self.root.after(1000,hideMsg)
                        Camera2.pack()

                    messagebox.showerror("Error!", "An Error Occurred. Please Make sure your Webcam is accessible and try again")
                    retry_btn = tk.Button(WebCamFrame,text="Retry",command=retried)
                    retry_btn.pack()
                    retry_btn.focus()
                    label.pack_forget()  # Remove existing label
                    Camera2.pack_forget()  # Remove existing Camera2 button
                    camIsOpen = True
                    return
                # CameraMsg.pack()
                Camera2.pack()
                Camera2.focus()

                for code in decode(img):
                    decoded_data = code.data.decode("utf-8")
                    rect_pts = code.rect

                    if decoded_data:
                        pts = np.array([code.polygon], np.int32)
                        cv2.polylines(img, [pts], True, (0, 0, 255), 3)
                        cv2.putText(img, str(decoded_data), (rect_pts[0], rect_pts[1]), cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (127, 127, 127), 2)

                        # Check if the detected data is a valid URL
                        if is_valid_url(decoded_data):
                            if not self.url_opened:
                                def url_restore():
                                    self.url_opened = False
                                response = messagebox.askyesno(f"Location Redirect","This QR wants to redirect you to:\n"+decoded_data+"\n Allow?")
                                if response == 1:
                                    # Open browser only once for the first valid URL detected
                                    webbrowser.open_new_tab(decoded_data)
                                    self.url_opened = True
                                    self.root.after(9000,url_restore)
                                    decoded_data = ""  # Reset decoded_data to prevent repeated opening
                                    closeWebcam()
                                else:
                                    pass

                # Display the webcam feed inside the existing label widget
                img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(img)
                img = ImageTk.PhotoImage(img)
                label.config(image=img)
                label.image = img

            # Cleanup after closing the webcam
            closeWebcam()
            cam.release()
            cv2.destroyAllWindows()
            label.pack_forget()  # Remove label after closing the webcam
            Camera.pack(side=tk.BOTTOM, pady=120)  # Reposition the Camera button
            # Camera2.pack(side=tk.BOTTOM, pady=10)  # Reposition the Camera2 button
        
        if not camIsOpen:
            Camera = tk.Button(WebCamFrame, text="Open Webcam", command=openWebCam)
            Camera.pack(side=tk.BOTTOM, pady=120)
        # endregion webcam
        
    def browse_qr(self):
        global selected_dir, img
        new_selected_dir = filedialog.askopenfilename(filetypes=[("PNG", "*.png"),("JPEG", "*.jpeg"),("JPG", "*.jpg"),("Bitmap","*bmp")])
        if new_selected_dir:  # Check if a file was selected
            selected_dir = new_selected_dir
            try:
                img = Image.open(selected_dir)
                img = img.resize((100, 100), Image.LANCZOS)
                img = ImageTk.PhotoImage(img)
                self.file_name = os.path.basename(selected_dir)
                self.directory_path_label.config(text=f"Selected File: {self.file_name}")
                self.extract_button.config(state=tk.NORMAL)
                self.PreviewQR.config(image=img)
                self.PreviewQR.image = img  # Keep a reference to avoid garbage collection
            except AttributeError:
                pass

    def extract_button(self):
        self.infoFrame.pack(pady=30)
        img = cv2.imread(selected_dir)
        detector = cv2.QRCodeDetector()
        data = detector.detectAndDecode(img)
        self.QRInfo.config(state=tk.NORMAL)
        self.QRInfo.insert(1.0,data[0])
        self.QRInfo.config(state=tk.DISABLED)
        self.clear_button.pack(side=tk.BOTTOM)

    def clearTextbox(self):
        self.QRInfo.config(state=tk.NORMAL)
        self.QRInfo.delete('1.0', 'end')
        self.QRInfo.config(state=tk.DISABLED)

    def saveQr(self):
        qr_data = self.data.get('1.0','end')
        if qr_data != "\n":
            qr = qrcode.make(qr_data)
            path = filedialog.asksaveasfilename(filetypes=[("PNG Image","*.png"),("JPEG Image","*.jpeg"),("JPG Image","*.jpg"),("Bitmap Image","*.bmp")],defaultextension=".png")
            if path:
                qr.save(path)
                messagebox.showinfo("Success","Operation Completed Successfully")
                self.data.delete('1.0','end')
        else:
            messagebox.showwarning("Warning!","You can not crate an empty QR code in this app")

    def run(self):
        self.root.mainloop()
    
if __name__ == "__main__":
    app = QRAnalyzer()
    app.run()