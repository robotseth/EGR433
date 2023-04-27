import pyqtgraph as pg
from PyQt5.QtWidgets import QApplication
import numpy as np

# create a new application
app = QApplication([])

# create a plot window
win = pg.GraphicsWindow(title='Live Plot')

# create a plot curve
curve = win.addPlot()

# create a data array
data = np.random.normal(size=(10,))

# define an update function
def update():
    global curve, data
    data[:-1] = data[1:]
    data[-1] = np.random.normal()
    curve.setData(data)

# start a timer to update the plot
timer = pg.QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

# start the application event loop
app.exec_()
