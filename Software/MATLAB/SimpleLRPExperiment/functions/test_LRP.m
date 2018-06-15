% test_LRP - Tests whether LRP works like expected.
% In particular the focus is on the relevance conservation principle.
% **************************************************************************
% function [vSwapped] = test_LRP(v)
%
% author: Joost Berkhout, CWI
% date created: 14-6-2018
% last modification date: 
% modification details: 
%**************************************************************************
% INPUTS:
% or_data       original data of size 1 x image_dimensions_product
% data          input data of size 1 x image_dimensions_product(after normalization)
% im_dim        image dimentions (original small images) vector
% model         pre-trained model NNet
% lrp_method    method for relevance propagation, one of 3@
%               1 = ratio local and global pre-activtatons (Eq(56) from paper)
%               2 = Using stabilizer  epsilon: 1 (Eq(58) from paper)
%               3 = LRP: Using alpha-beta rule: 2 (Eq(60) from paper)
% select        vector indicating the selected class of to computer relevance against
% shape_labels  the shape label codes
%**************************************************************************
% OUTPUTS:
% [] - ...
%**************************************************************************
% NOTES: 
% See also Issue #23 on Github: https://github.com/NLeSC/XAI/issues .
%**************************************************************************
% EXAMPLES USAGE: 
%**************************************************************************
% REFERENCES:
%**************************************************************************
function [] = test_LRP(or_data, data, im_dim, model, ...
                       lrp_method, select, shape_labels)
                                      
% pass the image as described by data through the pre-trained model
pred_classes = model.forward(data);
[~, index_pred_class] = max(pred_classes);
pred_class = shape_labels(index_pred_class);

% get some info about neural network
numb_layers = size(model.modules, 2);

% evaluate lrp for the last layer
disp('Select is: ')
disp(select)
disp('The prediction is: ')
disp(pred_classes)

disp('Regarding last layer:')
disp('=====================')
last_layer = model.modules{numb_layers};
X = last_layer.X;
Y = last_layer.Y;
disp('The X values at the last layer are: ')
disp(X)
disp('The Y values at the last layer is: ')
disp(Y)
disp('Manually calculating the Y values (via softmax) gives: ')
expX = exp(X);
disp(expX/sum(expX));
disp('LRP scores (R) at the last layer given backwards (I think it should be Y, see also lrp_cnn_demo.m, Q: is this correctly implemented in our code??): ')
lrp_scores = last_layer.lrp(Y, 'alphabeta', 2);
disp(lrp_scores)
disp('LRP scores (R) are calculated by Y .* X, in particular: ')
disp(Y .* X)
disp('The original R-sum is: ')
disp(sum(Y))
disp('After LRP the R-sum is: ')
disp(sum(lrp_scores))
disp('Conclusions: the relevance conservation principle does not seem to holds for the original LRP toolbox code...')
disp('However, when I uncommented the lrp function in softmax() it does give the right results!')

end
