import tkinter as tk
import pandas as pd

csvData = pd.read_csv("assets.csv")
columns = list(csvData)

class Options(tk.Frame):
    # Initialise main options window
    def __init__(self, root):
        tk.Frame.__init__(self, root)

        root.title("Gem Options")
        root.geometry("400x400")
        b1 = tk.Button(self, text="View Gems", width = 20, command=Window1(self).ViewGems)
        b1.grid(row = 1, column = 4)
        b2 = tk.Button(self, text="Add Gems", width = 20, command=Window2(self).AddGems)
        b2.grid(row = 2, column = 4)

class Window1(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)
        
        # Gem and cut values stored in arrays for future use
        self.gemValues = [15, 20, 25, 30, 47.5, 80, 150, 225, 575, 1425, 21, 44, 435, 32, 65, 21, 180, 14, 67.5, 200, 100, 1775, 400, 51, 287.5, 525, 615, 70]
        self.cutValues = [1, 1.25, 1.5, 1.75, 2, 2.3, 2.6, 3.5, 5, 2.4, 69, 10, 4, 3, 0, 5, 5]

    # Window to view gems and value in Simoleons
    def ViewGems(self):
        self.window1 = tk.Toplevel(self)
        self.window1.title("Gems")
        self.window1.geometry("1500x700")

        # Display as labels in a grid
        for x in range(0, 18):
            col = columns[x]
            if x == 0:
                myWidth = 14
            else:
                myWidth = 10
            # Column names
            label = tk.Label(self.window1, width = myWidth, height = 1, text = col)
            label.grid(row = 0, column = x)
            for y in range(0, 28):
                label = tk.Label(self.window1, width = myWidth, height = 1, text = csvData[col][y])
                label.grid(row = y+1, column = x)

            sumTotal = csvData.sum(axis=1).sum()
            totalSimoleons = self.totalAll()

            self.SumGems(sumTotal)
            self.NumerousGems()
            self.TotalValueGems(totalSimoleons)
            self.AverageValueGems(sumTotal, totalSimoleons)
        
    def SumGems(self, sumTotal):
        # Calculate sum of gems
        sumLabel = tk.Label(self.window1, width = 15, height = 1, text = "Total Gems:")
        sumLabel.grid(row = 1, column = 18)
        sumLabelValue = tk.Label(self.window1, width = 15, height = 1, text = sumTotal)
        sumLabelValue.grid(row = 2, column = 18)

    def NumerousGems(self):
        # Most numerous gem
        maxValue = csvData.sum(axis=1).idxmax()
        maxLabel =  tk.Label(self.window1, width = 15, height = 1, text = "Most Numerous:")
        maxLabel.grid(row = 3, column = 18)
        maxLabelValue = tk.Label(self.window1, width = 15, height = 1, text = csvData['*'][maxValue])
        maxLabelValue.grid(row = 4, column = 18)

    def TotalValueGems(self, totalSimoleons):
        # Total value of all gems
        simLabel = tk.Label(self.window1, width = 15, height = 1, text = "Total (Simoleons):")
        simLabel.grid(row = 5, column = 18)
        simLabelValue = tk.Label(self.window1, width = 15, height = 1, text = int(round(totalSimoleons)))
        simLabelValue.grid(row = 6, column = 18)

    def AverageValueGems(self, sumTotal, totalSimoleons):
        if sumTotal != 0 and totalSimoleons != 0:
            # Average value of all gems
            avLabel = tk.Label(self.window1, width = 15, height = 1, text = "Average Value:")
            avLabel.grid(row = 7, column = 18)
            avLabelValue = tk.Label(self.window1, width = 15, height = 1, text = int(round(totalSimoleons/sumTotal)))
            avLabelValue.grid(row = 8, column = 18)

    # Calculate total value of all gems
    def totalAll(self):
        calcTotal = 0
        for x in range(1, 18):
            col = columns[x]
            for y in range(0, 28):
                cellCalc = csvData[col][y] * self.gemValues[y] * self.cutValues[x-1]
                calcTotal = calcTotal + cellCalc
        return calcTotal

class Window2(tk.Frame):
    def __init__(self, root):
        tk.Frame.__init__(self, root)

    # Window to add and remove gems from the csv file
    def AddGems(self):
        self.window2 = tk.Toplevel(self)
        self.window2.title("Add Gems")
        self.window2.geometry("1400x700")

        # Dictionary for SpinBox names
        self.spinNames = dict()

        # Control buttons
        Button = tk.Button(self.window2, width = 15, height = 1, text = "Refresh", command=lambda: self.Refresh())
        Button.grid(row = 1, column = 0)

        # Loop through CSV and set values as Spinboxes
        for x in range(0, 18):
            col = columns[x]
            if x == 0:
                myWidth = 15
            else:
                myWidth = 8
            # Column names
            label = tk.Label(self.window2, width = myWidth, height = 1, text = col)
            label.grid(row = 0, column = x+1)
            for y in range(0, 28):
                if x == 0:
                    Label = tk.Label(self.window2, width = myWidth, height = 1, text = csvData[col][y])
                    Label.grid(row = y+1, column = x+1)
                else:
                    # Create Spinbox with name from dictionary
                    spinName = ("spin" + str(x) + "_" + str(y))
                    # Set default value of Spinbox
                    defaultValue = tk.StringVar()
                    defaultValue.set(str(csvData[col][y]))
                    self.spinNames[spinName] = tk.Spinbox(self.window2, from_=0, to=1000, width=8, state='readonly', textvariable=defaultValue, command=lambda x=x, y=y, spinName=spinName: self.Enter(x, y, spinName))
                    self.spinNames[spinName].grid(row = y+1, column = x+1)

    # Take in coordinates and Spinbox entry and edit source csv file
    def Enter(self, x, y, spinName):
        mySpinbox = self.spinNames[spinName].get()
        col = columns[x]
        csvData.at[y,col] = mySpinbox
        csvData.to_csv('assets.csv', index=False)

    # Refresh AddGems window
    def Refresh(self):
        self.window2.destroy()
        self.window2.after(0, self.AddGems())