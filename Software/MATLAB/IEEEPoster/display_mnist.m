% script for displaying MNIST digits (using LRP toolbox)

clear
import data_io.*
import render.*

path = fullfile('C:','Projects','eStep','XAI','Software','lrp_toolbox-1.2.0','data','MNIST');


% load MNIST test data
mnist = data_io.read(fullfile(path,'test_images.mat'));
labels = data_io.read(fullfile(path,'test_labels.mat'));


% display 10 of a given digit
 for l = 0:9
         
     label1 = (labels==l);
     mnist1 = mnist(label1,:,:,:);
    
     %subplot_tight(10,1,l+1,[0.01]); 
     figure
     
    for c = 1:3
        
        digit = mnist1(c,:,:,:);
        
        %render input and heatmap as rgb images
        digit = render.digit_to_rgb(digit,3);

        digits{c} = digit;
    end

    img = render.save_image(digits,['digits' num2str(l) '.png']);
    imshow(img); axis off ; drawnow;    

end
    