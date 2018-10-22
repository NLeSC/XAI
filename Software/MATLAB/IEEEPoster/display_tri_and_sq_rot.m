% script for displaying Triangles and Squares dataset (using LRP toolbox)

clear
import data_io.*
import render.*

path = fullfile('C:\','Projects','eStep','XAI','Data','TrianglesAndSquaresRotation','Gray');


% load MNIST test data
tri_sq_test = data_io.read(fullfile(path,'TrianglesAndSquares_images_test_10k.mat'));
labels = data_io.read(fullfile(path,'TrianglesAndSquares_labels_test_10k.mat'));


% display 10 of a given digit
 for l = 0:2:2
         
     label1 = (labels==l);
     tens1 = tri_sq_test(label1,:,:,:);
    
     %subplot_tight(10,1,l+1,[0.01]); 
     figure
     
    for c = 1:10
        
        shape = tens1(c,:,:,:);
        
        %render input and heatmap as rgb images
        shape = render.shape_to_rgb(round(shape*255),3);

        shapes{c} = shape;
    end
    img = render.save_image(shapes,['shapes' num2str(l) '.png']);
    imshow(img); colormap(gray); axis off ; drawnow;    

end
    