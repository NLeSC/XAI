% visualize_1shape - visualize 1 shape from the simple shapes datasets
% **************************************************************************
% function [] = visualize_1shape(shape_images, shape_label, num2display, ...
%                   start_index, step)
%
% author: Elena Ranguelova, NLeSc
% date created: 02-02-2018
% last modification date: 24-05-2018
% modification details: made it generic for more shape datasets
%**************************************************************************
% INPUTS:
% shape_images   matrix containing  images from one shape
% shape_label    the label of the shape: 0-square, 1- circle, 2- triangle
% num2display    number of imges to display in 1 figure
% start_index    the index of the first image to display
% step           the index step betweeen 2 images to display
%**************************************************************************
% OUTPUTS:
%**************************************************************************
% NOTES:
%**************************************************************************
% EXAMPLES USAGE:
%
% see test_sort_contrast.m or demo_lrp_exp_lenet_*.m
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [] = visualize_1shape(shape_images, shape_label, num2display, ...
    start_index, step)


%% check input parameters => error
num_images = size(shape_images,1);
if (num2display > num_images) || (start_index + num2display*step > num_images)
    error("The number or index of images to display exeeds the total number of shape images!");
elseif num2display > 30
    error("The number of images to display exeeds the number of images to dusplay in 1 figure!");
end

%% figure and subplots
figure('units','normalized','outerposition',[0 0 1 1]);
subplts = numSubplots(num2display);
sbplt_rows = subplts(1); sbplt_cols = subplts(2);
%% visualize

count = 0;
for i = 1:step:num2display*step
    %disp(['Start_index + i:', num2str(start_index + i)]);
    count = count + 1;
    subplot(sbplt_rows, sbplt_cols,count);
    shape = reshape(shape_images(start_index + i,:),32,32);
    imshow(shape);
    hold on;
end
hold off;

switch shape_label
    case 0
        shape_type = 'square';
    case 1
        shape_type = 'circle';
    case 2
        shape_type = 'triangle';
end

title_str = ['Test set: 15 ' shape_type ' images starting at image ' num2str(start_index) ' with step of ' num2str(step)];
axes('Position',[0 0 1 1],'Xlim',[0 1],'Ylim',[0  1],'Box','off','Visible','off','Units','normalized', 'clipping' , 'off');
t = text(0.5, 0.98,title_str); t.FontSize = 14; t.FontWeight = 'bold';
