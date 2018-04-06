% amat_loader - function to load data from the amat format
% **************************************************************************
% function [images, labels, colors, centroids] = amat_loader(amat_filename)
%
% author: Elena Ranguelova, NLeSc
% date created: 23.03.2018
% last modification date: 06-04-2018
% modification details: returns centroids of the shape
%**************************************************************************
% INPUTS:
% amat_filename an .amat (ascii format) file containing BabyAIShapes dataset
%**************************************************************************
% OUTPUTS:
% images        matrix of size num_images x image_dimentions_product containing the raw pixel values
% labels        column vector of size num_images x 1 containing the shape labels 
% colors        column vector of size num_images x 1 containing the shape colors 
% centroids     column vector of size num_imahes x 2 containing the
%               (x,y)coords of the shape centroid
%**************************************************************************
% NOTES: This function is closely related to the <BabyAIShapes datasets>:
% http://www.iro.umontreal.ca/~lisa/twiki/bin/view.cgi/Public/BabyAIShapesDatasets
% The .amat file is an ascii format. The value separator is the space (ascii code 0x20) It is organized as follows:
% 
% The first line is the number of examples and the number of values per line (1031).
% On each subsequent line, the first 1024 values represent the gray tone of each pixel 
% (or the color, depending on how you interpret it) as a floating point value between 0 and 1, inclusively (32 lines of 32 pixels). 
% The next 7 values are:
% The shape: 0=rectangle, 1=ellipse and 2=triangle
% The color of the shape: this is actually an integer between 0 and 7. Divide by 7 to get the corresponding gray tone. 
% # List of colors. The position of a color in that list is the integer index that will be associated to it.
% palette = [[0,0,0], [255,0,0], [0,255,0], [0,0,255], [255,255,0], [255,0,255], [0,255,255], [255,255,255]]
% # Names of the colors in the palette.
% color_names = ['black', 'red', 'green', 'blue', 'yellow', 'magenta', 'cyan', 'white']
%**************************************************************************
% EXAMPLES USAGE: 
% 
% see test_amat_loader.m
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [images, labels, colors, centroids] = amat_loader(amat_filename)

delimiterIn = ' ';
headerlinesIn = 1;
import_data = importdata(amat_filename,delimiterIn,headerlinesIn);
images = import_data.data(:,1:1024);
labels = import_data.data(:,1025);
colors = import_data.data(:,1026);
centroids = [import_data.data(:,1027) import_data.data(:,1028)];
