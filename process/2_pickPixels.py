from tkinter import * 
from tkinter import ttk
from PIL import Image,ImageTk 
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.figure import Figure
import math
import cv2 
import numpy as np
import sys
import os
import csv
import pickle

WAVELENGTHS = [391.3, 392.62, 393.93, 395.24, 396.56, 397.87, 399.18, 400.5, 401.81, 403.12, 404.44, 405.75, 407.06, 408.38, 409.69, 411.0, 412.32, 413.64, 414.95, 416.26, 417.58, 418.9, 420.21, 421.52, 422.84, 424.16, 425.47, 426.79, 428.1, 429.42, 430.74, 432.05, 433.37, 434.68, 436.0, 437.32, 438.64, 439.95, 441.27, 442.59, 443.9, 445.22, 446.54, 447.86, 449.18, 450.49, 451.81, 453.13, 454.45, 455.77, 457.09, 458.4, 459.72, 461.04, 462.36, 463.68, 465.0, 466.32, 467.64, 468.96, 470.28, 471.6, 472.92, 474.24, 475.56, 476.88, 478.2, 479.52, 480.84, 482.17, 483.49, 484.81, 486.13, 487.45, 488.77, 490.1, 491.42, 492.74, 494.06, 495.38, 496.71, 498.03, 499.35, 500.67, 502.0, 503.32, 504.64, 505.97, 507.29, 508.62, 509.94, 511.26, 512.59, 513.91, 515.24, 516.56, 517.88, 519.21, 520.53, 521.86, 523.18, 524.51, 525.83, 527.16, 528.48, 529.81, 531.14, 532.46, 533.79, 535.12, 536.44, 537.77, 539.1, 540.42, 541.75, 543.08, 544.4, 545.73, 547.06, 548.38, 549.71, 551.04, 552.36, 553.69, 555.02, 556.35, 557.68, 559.0, 560.34, 561.66, 563.0, 564.32, 565.65, 566.98, 568.31, 569.64, 570.97, 572.3, 573.63, 574.96, 576.29, 577.62, 578.95, 580.28, 581.61, 582.94, 584.27, 585.6, 586.93, 588.26, 589.6, 590.93, 592.26, 593.59, 594.92, 596.26, 597.58, 598.92, 600.26, 601.58, 602.92, 604.25, 605.58, 606.92, 608.25, 609.58, 610.92, 612.25, 613.58, 614.92, 616.25, 617.58, 618.92, 620.26, 621.58, 622.92, 624.26, 625.59, 626.92, 628.26, 629.6, 630.93, 632.26, 633.6, 634.93, 636.28, 637.61, 638.94, 640.29, 641.62, 642.95, 644.3, 645.62, 646.96, 648.31, 649.64, 650.97, 652.32, 653.66, 654.98, 656.32, 657.66, 659.0, 660.34, 661.68, 663.02, 664.36, 665.7, 667.04, 668.38, 669.7, 671.04, 672.38, 673.72, 675.06, 676.4, 677.74, 679.08, 680.42, 681.76, 683.1, 684.44, 685.79, 687.12, 688.46, 689.8, 691.15, 692.5, 693.84, 695.18, 696.52, 697.86, 699.2, 700.54, 701.88, 703.22, 704.56, 705.9, 707.26, 708.6, 709.94, 711.28, 712.62, 713.96, 715.31, 716.66, 718.0, 719.34, 720.68, 722.03, 723.38, 724.71, 726.06, 727.4, 728.74, 730.1, 731.44, 732.79, 734.12, 735.47, 736.82, 738.16, 739.51, 740.86, 742.2, 743.54, 744.9, 746.24, 747.58, 748.93, 750.28, 751.62, 752.97, 754.32, 755.66, 757.02, 758.36, 759.7, 761.06, 762.4, 763.75, 765.1, 766.44, 767.8, 769.14, 770.49, 771.84, 773.19, 774.54, 775.88, 777.24, 778.58, 779.94, 781.29, 782.64, 783.98, 785.33, 786.68, 788.03, 789.38, 790.74, 792.08, 793.44, 794.79, 796.14, 797.48, 798.84, 800.19, 801.54, 802.89, 804.24, 805.6, 806.94, 808.3, 809.65, 811.0, 812.36, 813.71, 815.06, 816.41, 817.76, 819.12, 820.47, 821.82, 823.18, 824.53, 825.88, 827.24, 828.59, 829.95, 831.3, 832.66, 834.01, 835.36, 836.72, 838.08, 839.43, 840.78, 842.14, 843.5, 844.85, 846.2, 847.56, 848.92, 850.27, 851.63, 852.98, 854.34, 855.7, 857.05, 858.41, 859.77, 861.12, 862.48, 863.84, 865.2, 866.55, 867.91, 869.27, 870.63, 871.98, 873.34, 874.7, 876.06, 877.42, 878.78, 880.13, 881.49, 882.85, 884.21, 885.57, 886.93, 888.29, 889.65, 891.01, 892.37, 893.73, 895.09, 896.45, 897.81, 899.17, 900.53, 901.89, 903.25, 904.61, 905.97, 907.33, 908.7, 910.06, 911.42, 912.78, 914.14, 915.5, 916.86, 918.23, 919.59, 920.95, 922.32, 923.68, 925.04, 926.4, 927.77, 929.13, 930.49, 931.86, 933.22, 934.58, 935.95, 937.31, 938.68, 940.04, 941.4, 942.77, 944.13, 945.5, 946.86, 948.23, 949.59, 950.96, 952.32, 953.69, 955.06, 956.42, 957.79, 959.15, 960.52, 961.88, 963.25, 964.62, 965.98, 967.35, 968.72, 970.08, 971.45, 972.82, 974.19, 975.56, 976.92, 978.29, 979.66, 981.02, 982.4, 983.76, 985.13, 986.5, 987.87, 989.24, 990.6, 991.98, 993.34, 994.71, 996.08, 997.45, 998.82, 1000.19, 1001.56, 1002.93, 1004.3, 1005.67, 1007.04, 1008.42, 1009.79]

class GUI(Canvas):
    def __init__(self, master, *args, **kwargs):
        Canvas.__init__(self, master, *args, **kwargs)

        self.master = master	
        self.master.geometry('+1+30')
        self.FACTOR = 20
        self.my_canvas = Canvas(self.master)
        self.my_canvas.grid(row=0, column=0, rowspan=11)

        self.my_canvas.configure(width=y_plate, height=x_plate)
        self.plate_container = self.my_canvas.create_image(0,0,anchor=NW,image=plate) 

        self.my_canvas.bind('<Button 1>', self.open_selected_contour)
        self.chosenPixel = (-1,-1)
        self.output = [ [] for _ in range(len(contours)) ]

        self.figure = Figure(figsize=(5,3), dpi = 100)
        self.sub_plot = self.figure.add_subplot(111)
        self.sub_plot.axvline(x=WAVELENGTHS[189], color='r')
        self.sub_plot.axvline(x=WAVELENGTHS[121], color='g')
        self.sub_plot.axvline(x=WAVELENGTHS[53], color='b')
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().grid(row=0, column=1, columnspan=2, rowspan=5)

        self.genus_button = Button(self.master, text="Select all in genus:", command = self.select_genus)
        self.genus_button.grid(row=5, column=1)

        self.genus_name = StringVar()
        self.drop_down = ttk.Combobox(self.master, textvariable=self.genus_name, width=20)
        self.drop_down['values'] = colonyGenuses
        self.drop_down.grid(row=5, column=2)

        self.check_hl_flag = True
        self.check_hl = Button(self.master, text='Highlight Selection', command = self.hl_selection_button)
        self.check_hl.grid(row=6, column=1)

        clear_button = Button(self.master, text="Clear Selection", command = self.clear_output)
        clear_button.grid(row=6, column=2)

        generate_button = Button(self.master, text="Generate Suggested Pixels", command = self.generate_pixels)
        generate_button.grid(row=7, column=1)

        cycle_button = Button(self.master, text="Cycle through selected contours", command = self.cycle)
        cycle_button.grid(row=7, column=2)

        self.t1 = StringVar()
        self.goto_button = Button(self.master, text="Go to contour #: ", command=lambda: self.open_sub_window(int(self.t1.get()) - 1))
        self.goto_button.grid(row=8, column=1, sticky="e")

        validate_cmd = (self.register(self.callback))		

        self.goto_entry = Entry(self.master, validate='all', validatecommand=(validate_cmd, '%P'), textvariable=self.t1)
        self.goto_entry.grid(row=8, column=2, sticky="w")

        plot_button = Button(self.master, text="Plot selected pixels", command = self.plot_selected)
        plot_button.grid(row=9, column=1)

        clear_plot_button = Button(self.master, text="Clear Plot", command=self.clear_plot)
        clear_plot_button.grid(row=9, column=2)

        save_button = Button(self.master, text="Save Complete Output", command = self.save_output)
        save_button.grid(row=10, column=1)

        self.hl_selection_button()

    def callback(self, P):
        return str.isdigit(P) and int(P) < len(contours) + 1 or str(P) == ""

    def clear_output(self):
        self.output = [ [] for _ in range(len(contours)) ]
        self.highlight_selection()
        self.count = None

    def save_output(self):
        if not os.path.isdir(PLATE_NAME + "/hyper_colonies"):
            os.system("mkdir " + PLATE_NAME + "/hyper_colonies")
        for i in range(len(contours)):
            if len(self.output[i]) > 0:
                out = []
                for pair in self.output[i]:
                    out.append(np.append(np.array(pair), data[pair]))
                np.savetxt(PLATE_NAME + "/hyper_colonies/" + PLATE_NAME + "_" + str(i + 1) + ".csv", out, delimiter=",", fmt="%i")	

    def updateTextBox(self):
        self.text.delete('1.0', END)
        for outlist in self.output:
            for pair in outlist:
                self.text.insert(END, "\n" + str(pair[0]) + " , " + str(pair[1]))

    def generate_pixels(self):
        for i in range(len(contours)):
            M = cv2.moments(contours[i])
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            self.output[i].append((cY,cX))
            self.output[i].append((cY,cX + 1))
            self.output[i].append((cY,cX - 1))
            self.output[i].append((cY + 1,cX))
            self.output[i].append((cY + 1,cX + 1))
            self.output[i].append((cY + 1,cX - 1))
            self.output[i].append((cY - 1,cX))
            self.output[i].append((cY - 1,cX + 1))
            self.output[i].append((cY - 1,cX - 1))
        self.highlight_selection()
        #self.updateTextBox()	

    def open_selected_contour(self, event):
        for i in range(len(contours)):
            if cv2.pointPolygonTest(contours[i], (event.x, event.y), measureDist=False) > 0:
                self.open_sub_window(i)
                break

    def cycle(self):
        self.count = None

        def nextContour():
            for i in range(self.count + 1, len(self.output)):
                if self.output[i] != []:
                    self.count = i
                    break
            self.top.destroy()
            self.open_sub_window(self.count)
            add_buttons()

        def prevContour():
            for i in range(self.count - 1, -1, -1):
                if self.output[i] != []:
                    self.count = i
                    break
            self.top.destroy()
            self.open_sub_window(self.count)
            add_buttons()

        def add_buttons():
            next_button = Button(self.top, text = "Next contour", command = nextContour)
            prev_button = Button(self.top, text = "Previous contour", command = prevContour)
            next_button.pack()
            prev_button.pack()

        for i in range(len(self.output)):
            if self.output[i] != []:
                self.count = i
                break
        if self.count != None:
            self.open_sub_window(self.count)
            add_buttons()

    def highlight_selection(self):
        self.copy_image = np.copy(image)
        if self.check_hl_flag:
            for i in range(len(self.output)):
                for pair in self.output[i]:
                    self.copy_image[pair] = (0,255,0)
        self.new_plate = ImageTk.PhotoImage(image=Image.fromarray(np.flip(self.copy_image.astype(np.uint8), 2)))
        self.my_canvas.itemconfig(self.plate_container, image=self.new_plate)

    def hl_selection_button(self):
        if self.check_hl_flag:
            self.check_hl_flag = False
        else:		
            self.check_hl_flag = True
        self.highlight_selection()

    def select_genus(self):
        for colony in colonyMatch[self.genus_name.get()]:
            M = cv2.moments(contours[colony])
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            self.output[colony].append((cY,cX))
            self.output[colony].append((cY,cX + 1))
            self.output[colony].append((cY,cX - 1))
            self.output[colony].append((cY + 1,cX))
            self.output[colony].append((cY + 1,cX + 1))
            self.output[colony].append((cY + 1,cX - 1))
            self.output[colony].append((cY - 1,cX))
            self.output[colony].append((cY - 1,cX + 1))
            self.output[colony].append((cY - 1,cX - 1))
        self.highlight_selection()

    def clear_plot(self):
        self.sub_plot.clear()
        self.figure_canvas = FigureCanvasTkAgg(self.figure, self.master)
        self.figure_canvas.draw()
        self.figure_canvas.get_tk_widget().grid(row=0, column=1, columnspan=2, rowspan=5)

    def plot_selected(self):
        for contour in self.output:
            for pair in contour:
                self.sub_plot.plot(WAVELENGTHS,	data[pair])
                self.sub_plot.axvline(x=WAVELENGTHS[189], color='r')
                self.sub_plot.axvline(x=WAVELENGTHS[121], color='g')
                self.sub_plot.axvline(x=WAVELENGTHS[53], color='b')
                self.figure_canvas = FigureCanvasTkAgg(self.figure, self.master)
                self.figure_canvas.draw()
                self.figure_canvas.get_tk_widget().grid(row=0, column=1, columnspan=2, rowspan=5)


    def open_sub_window(self, num):			
        def resize_array(data,factor):
            x,y,z = np.shape(data)
            new = np.zeros((factor * x, factor * y, z))
            for i in range(x):
                for j in range(y):
                    for k in range(factor):
                        for l in range(factor):
                            new[ (i * factor) + k ][ (j * factor) + l ] = data[i][j]
            return new	

        def updateImage(num): 
            self.sub_Data = np.copy(self.sub_Data_copy)
            for pair in self.output[num]:
                self.sub_Data[pair[0] - min_sample, pair[1] - min_line] = (0,255,0)
            self.newsubImage = makeImage(self.sub_Data)
            self.subWindow.itemconfig(self.image_container, image=self.newsubImage)

        def updateChosenPixel(x,y):
            self.chosenPixel = (min_sample + int(y / self.FACTOR), min_line + int(x / self.FACTOR))
            self.sub_plot.plot(WAVELENGTHS,	data[self.chosenPixel])
            self.sub_plot.axvline(x=WAVELENGTHS[189], color='r')
            self.sub_plot.axvline(x=WAVELENGTHS[121], color='g')
            self.sub_plot.axvline(x=WAVELENGTHS[53], color='b')
            self.figure_canvas = FigureCanvasTkAgg(self.figure, self.master)
            self.figure_canvas.draw()
            self.figure_canvas.get_tk_widget().grid(row=0, column=1, columnspan=2, rowspan=5)
            changeOutput()


        def save_out(): #change to be customizable
            out = []
            for pair in self.output[num]:
                out.append(data[pair[0],pair[1]])
            np.savetxt(PLATE_NAME + "/" + str(num) + ".csv", out, delimiter=",")	

        def clear_out():
            self.output[num] = []
            self.clear_plot()
            updateImage(num)

        def makeImage(data):
            preImage = resize_array(data, self.FACTOR)
            preImage = preImage.astype(np.uint8)	
            return ImageTk.PhotoImage(image=Image.fromarray(preImage))

        def changeOutput():
            if self.chosenPixel in self.output[num]: #remove from output
                self.output[num].remove(self.chosenPixel)
            else:
                self.output[num].append(self.chosenPixel)
            if not self.select_flag:
                #				self.updateTextBox()
                updateImage(num)

        def group_select(event):
            if self.select_flag:
                for i in range(min(event.x, self.x_start), math.ceil(max(event.x,self.x_start) / self.FACTOR) * self.FACTOR, self.FACTOR):
                    for j in range(min(event.y, self.y_start), math.ceil(max(event.y,self.y_start) / self.FACTOR) * self.FACTOR, self.FACTOR):
                        updateChosenPixel(i,j) 
#				self.updateTextBox()
                updateImage(num)
                self.select_flag = False
            else:
                self.x_start = event.x
                self.y_start = event.y
                self.select_flag = True	

        def updatePlateImage(num):
            for i in range(min_line, max_line):
                for j in range(min_sample, max_sample):
                    if cv2.pointPolygonTest(contours[num], (i,j), measureDist=False) > 0:
                        self.copy_image[j,i] = (0,0,255)	
            self.new_plate = ImageTk.PhotoImage(image=Image.fromarray(np.flip(self.copy_image.astype(np.uint8), 2)))
            self.my_canvas.itemconfig(self.plate_container, image=self.new_plate)

        def reset_plate(event):
            self.my_canvas.itemconfig(self.plate_container, image=plate)
            self.highlight_selection()

        def click(event):
            updateChosenPixel(event.x, event.y)	

        self.top = Toplevel(self.master)
        self.top.geometry('-50-150')
        self.top.title(str(num + 1))
        self.top.wait_visibility()
        self.top.grab_set() 

        self.top.bind("<Destroy>", reset_plate) 
        lines = []
        samples = []
        for point in contours[num]:
            lines.append(point[0][0])
            samples.append(point[0][1])

        max_line = max(lines)
        max_sample = max(samples)
        min_line = min(lines)
        min_sample = min(samples)

        self.x_start = -1
        self.y_start = -1
        self.select_flag = False	

        self.subWindow = Canvas(self.top)
        self.subWindow.pack()
        self.subWindow.configure(width=self.FACTOR * (max_line - min_line), height= self.FACTOR * (max_sample - min_sample))

        self.subWindow.bind("<Button 3>", group_select)
        self.subWindow.bind('<Button 1>', click);

        self.sub_Data = np.copy(data[min_sample : max_sample, min_line : max_line, (189,121,53)]) * 0.075 #0.031
        #implement brightness
        self.sub_Data_copy = np.copy(self.sub_Data)
        self.sub_Image = makeImage(self.sub_Data)
        self.image_container = self.subWindow.create_image(0,0,anchor=NW,image=self.sub_Image)

        output_button = Button(self.top, text="Save selected pixels of this colony", command = save_out)
        output_button.pack()

        clear_button = Button(self.top, text="Clear Selection or Exclude From Output", command = clear_out)
        clear_button.pack()

        clear_plot_button = Button(self.top, text="Clear plot", command = self.clear_plot)
        clear_plot_button.pack()

        updatePlateImage(num)		
        updateImage(num)

if __name__ == "__main__":
    PLATE_NAME = sys.argv[1]

    with open(PLATE_NAME + "/hyper_contours.pkl","rb") as f:
        contours = pickle.load(f)

    with open(PLATE_NAME + "/" + PLATE_NAME + "_cropped.pkl", "rb") as f:
        data = pickle.load(f)

    master_image = cv2.imread(PLATE_NAME + "/drawn_HSimage.jpg") * 1.50
    image = np.copy(master_image)
    colonyGenuses = []
    colonyMatch = {}
    if os.path.isfile(PLATE_NAME + "/match.csv"):
        with open(PLATE_NAME + "/match.csv") as file:
            matchFile = csv.reader(file)	
            if matchFile != None:
                next(matchFile,None)
                for row in matchFile:
                    if not row[3] in colonyMatch.keys():
                        colonyMatch[row[3]] = [int(row[1]) - 1]
                    else:
                        colonyMatch[row[3]].append(int(row[1]) - 1)
            for key in colonyMatch.keys():
                colonyGenuses.append(key)
    else: 
        matchFile = None

    root = Tk()
    plate = ImageTk.PhotoImage(image=Image.fromarray(np.flip(image.astype(np.uint8), 2)))
    x_plate, y_plate, bands = np.shape(image)
    app = GUI(root)
    root.mainloop()
