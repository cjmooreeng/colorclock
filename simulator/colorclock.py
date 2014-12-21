import time
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from ui_colorclock import Ui_MainWindow
import sip
    
class colorclock(QMainWindow, Ui_MainWindow):
	def __init__(self, parent=None):
		super(colorclock,self).__init__(parent)
		self.setupUi(self)
		
		self.simulated_time = 0
		
		self.kick_timer = QTimer(self)
		self.connect(self.kick_timer, SIGNAL("timeout()"), self.kickTimer)
		self.kick_timer.start()				
	
	def remapInt(self, input, input_min, input_max, output_min, output_max):
		input_range = (input_max - input_min)
		output_range = (output_max - output_min)
		
		return (input/float(input_range) * output_range)
	
	def kickTimer(self):	
		self.simulated_time += 1 # increment by a second
		
		self.text_ctl.setText(time.asctime())
		self.hours = time.localtime().tm_hour + (time.localtime().tm_min/60.0) + (time.localtime().tm_sec/(3600.0))
		self.minutes = time.localtime().tm_min + time.localtime().tm_sec/60.0
		self.seconds = time.localtime().tm_sec
		
		self.findColors()
	
	def findColors(self):
		red = self.remapInt(self.hours, 0, 24, 0, 255)
		green = self.remapInt(self.minutes, 0, 60, 0, 255)
		blue = self.remapInt(self.seconds, 0, 60, 0, 255)
		
		self.updateColor(self.hour_ctl, red, 0, 0)
		self.updateColor(self.minute_ctl, 0, green, 0)
		self.updateColor(self.second_ctl, 0, 0, blue)
		self.updateColor(self.combined_ctl, red, green, blue)
		
	def updateColor(self, widget, red, green, blue):
		rgb_string = "rgb(%d,%d,%d)" % (red, green, blue)
		widget.setStyleSheet("QProgressBar::chunk { background-color: %s;}" % rgb_string)

	def closeEvent(self, event):
		pass

if __name__ == "__main__":
	import sys
	import os
	print sys.argv

	app = QApplication(sys.argv)    
	app.setStyle("plastique")

	window = colorclock()

	window.show()
	app.exec_()


