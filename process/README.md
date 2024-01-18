#Integration of Hyperspectral Data into CAMII Pipeline

Required Starting Folder:
	-Name the folder the 8 character plate name i.e. S2R80105
	-In the folder just needs to be the .bil file sharing the same name i.e. S2R80105.bil
		-As well as folder named 'in' with the two CAMII images names <DATA_CUBE_NAME>_*.bmp i.e. S2R80105_20230413152022.bmp

>python3 0_setParams <DATA_CUBE_NAME>
>python3 1_imageProcess <DATA_CUBE_NAME>
>python3 2_pickPixels <DATA_CUBE_NAME>

First step creates the CAMII contours and opens a GUI where you can manually set the offset, mutiplier, and angle parameters.
	-Click the "Save Values?" button to save to a file called "parameters.txt". This is used in the next step
Second step uses the determined parameters to crop the entire datacube and produce a cropped numpy file, an updated contours file (hyper_contours.npy), and some images for inspect
Third step allow for pixels selection with the guidance of CAMII contours

An example folder is included here for testing:
>python3 0_setParams S2R80105
>python3 1_imageProcess S2R80105
>python3 2_pickPixels S2R80105

Possible Parameters:
LINE_MULT: 0.728
SAMPLE_MULT: 0.744
LINE_START: 218
SAMPLE_START: 187
ROT_ANGLE: 0.39
VERT_FLIP_FLAG: 0
HORI_FLIP_FLAG: 1

Afterwards, the .bil file may be discarded.
