function [comp_hm, net, rel_first_layer] = inspect_layer_with_lrp(net, data, or_data, im_dim, plot)
%INSPECT_LAYER_WITH_LRP Inspect the first layer of a neural network 
% using lrp. The neural network is captured in variable net and data
% contains the data that is under inspection. Variable or_data contains
% the original data. Variable im_dim is an array with image dimensions.

% init
first_layer = net.modules{1};
output_size = first_layer.n;
input_lrp = ones(output_size, 1);

% FOR INPUT_LRP = [1,1]

% evaluate lrp
pred_classes = net.forward(data);  % to populate net, right?
rel_first_layer = first_layer.lrp(input_lrp, 'alphabeta', 2);

% plot heatmap
inp_shape = reshape(or_data, im_dim);  % reshape the input data to an image
shape = render.shape_to_rgb(round(inp_shape*255), 3); % convert the relevance toan RGB image
shape = permute(shape, [2 1 3]);
cmap = jet(255);
hm = render.hm_to_rgb(rel_first_layer, data, 3, [], 2, cmap, true);
comp_hm = render.save_image({shape, hm},'../heatmap.png');

if plot
figure();
imshow(comp_hm); 
axis off; 
drawnow;

rel_first_layer = reshape(rel_first_layer, im_dim);
figure('units','normalized','outerposition',[0 0 1 1])
heatmap(rel_first_layer)
title('[1, 1]')
end

% FOR [1, 0]

% evaluate lrp
pred_classes = net.forward(data);  % to populate net, right?
rel_first_layer = first_layer.lrp([1, 0], 'alphabeta', 2);

% plot heatmap
inp_shape = reshape(or_data, im_dim);  % reshape the input data to an image
shape = render.shape_to_rgb(round(inp_shape*255), 3); % convert the relevance toan RGB image
shape = permute(shape, [2 1 3]);
cmap = jet(255);
hm = render.hm_to_rgb(rel_first_layer, data, 3, [], 2, cmap, false);
comp_hm = render.save_image({shape, hm},'../heatmap.png');

if plot
figure();
imshow(comp_hm); 
axis off; 
drawnow;

rel_first_layer = reshape(rel_first_layer, im_dim);
figure('units','normalized','outerposition',[0 0 1 1])
heatmap(rel_first_layer)
title('[1, 0]')

end

% FOR [0, 1]

% evaluate lrp
pred_classes = net.forward(data);  % to populate net, right?
rel_first_layer = first_layer.lrp([0, 1], 'alphabeta', 2);

% plot heatmap
inp_shape = reshape(or_data, im_dim);  % reshape the input data to an image
shape = render.shape_to_rgb(round(inp_shape*255), 3); % convert the relevance toan RGB image
shape = permute(shape, [2 1 3]);
cmap = jet(255);
hm = render.hm_to_rgb(rel_first_layer, data, 3, [], 2, cmap, false);
comp_hm = render.save_image({shape, hm},'../heatmap.png');

if plot
figure();
imshow(comp_hm); 
axis off; 
drawnow;

rel_first_layer = reshape(rel_first_layer, im_dim);
figure('units','normalized','outerposition',[0 0 1 1])
heatmap(rel_first_layer)
title('[0, 1]')
end

end

