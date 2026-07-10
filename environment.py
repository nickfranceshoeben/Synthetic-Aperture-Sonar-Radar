############### Different environmental classes are stored here, as is a function to draw a custom environment out of point scatterers. ###############################


import matplotlib.pyplot as plt
import numpy as np
import json

class Environment:
    
    def __init__(self):
        
        self.targets = []
        
        # Snap-to-grid settings
        self.snapEnabled = True
        self.gridSize = 0.1   # meters
        
    def addTarget(self, x, y, refl=1.0):
        #Add simple point scatterer
        self.targets.append({
            "x":x,
            "y":y,
            "refl":refl
        })
        
        return
    
    def snapPoint(self, x, y):

        if not self.snapEnabled:
            return x, y

        x = round(x / self.gridSize) * self.gridSize
        y = round(y / self.gridSize) * self.gridSize

        return x, y
        
    def plot(self):
        #Plot function
        
        self.fig, self.ax = plt.subplots(figsize=(8, 8))
        
        self.ax.set_title('Add point by clicking. Press "s" to save environment.')
        self.ax.set_xlabel(f'Snap-to-grid: {self.snapEnabled}')
        

        if self.targets:
            x = [t["x"] for t in self.targets]
            y = [t["y"] for t in self.targets]
            self.scatter = self.ax.scatter(x, y, color="red")
            self.ax.set_xlim(0, 10)
            self.ax.set_ylim(0, 10)
            self.ax.set_aspect("equal")
            self.ax.grid(True)
            
        self.ax.set_xticks(
            np.arange(0, 10+self.gridSize, self.gridSize)
        )

        self.ax.set_yticks(
            np.arange(0, 10+self.gridSize, self.gridSize)
        )
        
        self.ax.tick_params(
            left=False,
            bottom=False,
            labelleft=False,
            labelbottom=False
        )

        self.ax.grid(True)
        
        self.fig.canvas.mpl_connect(
            "button_press_event",
            self.onClick
        )
        
        self.fig.canvas.mpl_connect(
            "key_press_event",
            self.onKey
        )

        plt.show()
        
    def onKey(self,event):
        
        if event.key == 's':
            self.save()
            
        if event.key == 'z':
            self.undoLast()
            
        if event.key == 'h':
            self.snapEnabled = not self.snapEnabled
            print(f'Snap: {self.snapEnabled}')
            self.ax.set_xlabel(f'Snap-to-grid: {self.snapEnabled}')
            self.updatePlot()
        
    def onClick(self, event):
        # Function for what happens when you click
        if event.inaxes is None:
            return
        
         # Snap mouse location
        x, y = self.snapPoint(
            event.xdata,
            event.ydata
        )

        # Add point to clicked area
        if self.pointExists(x, y):
            print("Point already exists")
            return

        self.targets.append({
            "x": x,
            "y": y,
            "reflectivity": 1.0
        })
        
        self.updatePlot()

        #print(f'Added target: {self.targets[-1]}')
        
    def undoLast(self):

        if len(self.targets) > 0:
            removed = self.targets.pop()
            print(f"Removed {removed}")

            self.updatePlot()

        else:
            print("No points to remove")
            
    def pointExists(self, x, y, tolerance=1e-6):

        for target in self.targets:

            dx = target["x"] - x
            dy = target["y"] - y

            if (dx**2 + dy**2)**0.5 < tolerance:
                return True

        return False
            
    def updatePlot(self):
        
        # Extract coordinates from all targets
        x = [t["x"] for t in self.targets]
        y = [t["y"] for t in self.targets]

        # Update the scatter plot
        self.scatter.set_offsets(list(zip(x, y)))

        # Tell matplotlib to redraw
        self.fig.canvas.draw_idle()
        
    def save(self, filename="environment.json"):

        with open(filename, "w") as file:
            json.dump(self.targets, file, indent=4)

        print(f"Environment saved to {filename}")
        
    def load(self, filename="environment.json"):

        with open(filename, "r") as file:
            self.targets = json.load(file)

        print(f"Environment loaded from {filename}")