import sys
import os
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QDialog, QApplication, QFileDialog
from PyQt5.uic import loadUi
#import time, datetime
import telepot
from telepot.loop import MessageLoop
from PIL import ImageQt
import cv2
import numpy as np
from datetime import datetime

class MainWindow(QDialog):
    def __init__(self):
        super(MainWindow, self).__init__()
        loadUi("gui.ui", self)
        self.labelMsg = ""
        self.image_folder = "./imgs"  # Change this to your image folder path
        self.image_files = []
        self.current_index = 0
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_image)
       
        self.load_images()
        self.callTelegram()

        
    def action(self,msg):

        global command
        #now = datetime.datetime.now()
        chat_id = msg['chat']['id']
        command = msg['text']

        print ('Received: %s' % command)
        self.labelMsg = command
        self.label.setText(command)
        print(self.labelMsg)
        # image = self.label.pixmap()
        # print(image)
        # success = image.save('test.png')
        
    def callTelegram(self):    
        telegram_bot = telepot.Bot('6408009830:AAHUdrU6s4Hr5YHx5x_avkyCIEm_DkjsqLw')
    
        print (telegram_bot.getMe())
    
        MessageLoop(telegram_bot, self.action).run_as_thread()
    
        print ('Pi3LEDBot is Running....')    

    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Folder")
        if folder:
            self.image_folder = folder
            self.load_images()

    def load_images(self):
        self.image_files = [os.path.join(self.image_folder, file) for file in os.listdir(self.image_folder) if file.endswith(('.png', '.jpg', '.jpeg'))]
        if self.image_files:
            self.timer.start(10000)  # Start timer with 10 sec delay
            self.update_image()
            print(self.labelMsg)
            self.tim()
            #self.main()
            #self.test()
 



    def update_image(self):
        print(self.labelMsg)
        if self.image_files:
            if self.current_index == 0:
                self.label.setText(self.labelMsg)
                self.current_index = self.current_index + 1
            else:
                pixmap = QtGui.QPixmap(self.image_files[self.current_index])
                self.label.setPixmap(pixmap.scaled(self.label.size(), QtCore.Qt.KeepAspectRatio))
                self.current_index = (self.current_index + 1) % len(self.image_files)
    
    
        
        
    def tim(f):
        # Get current date and time
        current_datetime = datetime.now()
        current_date = current_datetime.strftime("%Y-%m-%d")
        current_time = current_datetime.strftime("%H:%M:%S")
        current_day = current_datetime.strftime("%A")

        # Create white background image
        width, height = 500, 250
        background_color = (255, 255, 255)  # White color
        image = np.full((height, width, 3), background_color, dtype=np.uint8)

        # Add date and time text to the image
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 1.5
        font_thickness = 2

        # Date text
        date_text = f"Date: {current_date}"
        date_text_size = cv2.getTextSize(date_text, font, font_scale, font_thickness)[0]
        date_text_x = int((width - date_text_size[0]) / 2)
        date_text_y = int(height / 4)
        cv2.putText(image, date_text, (date_text_x, date_text_y), font, font_scale, (0, 0, 0), font_thickness)

        # Time text
        time_text = f"Time: {current_time}"
        time_text_size = cv2.getTextSize(time_text, font, font_scale, font_thickness)[0]
        time_text_x = int((width - time_text_size[0]) / 2)
        time_text_y = int(height / 2)
        cv2.putText(image, time_text, (time_text_x, time_text_y), font, font_scale, (0, 0, 0), font_thickness)

        # Day text
        day_text = f"Day: {current_day}"
        day_text_size = cv2.getTextSize(day_text, font, font_scale, font_thickness)[0]
        day_text_x = int((width - day_text_size[0]) / 2)
        day_text_y = int(3 * height / 4)
        cv2.putText(image, day_text, (day_text_x, day_text_y), font, font_scale, (0, 0, 0), font_thickness)

        # Display the image
        #cv2.imshow("Date and Time", image)
        cv2.imwrite('imgs/tim.png', image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
        
app = QApplication(sys.argv)
mainwindow = MainWindow()
mainwindow.show()
mainwindow.showFullScreen()
sys.exit(app.exec_())
