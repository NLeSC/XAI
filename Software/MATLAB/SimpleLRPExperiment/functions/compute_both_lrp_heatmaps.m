% compute_both_lrp_heatmap - computes both LRP toolbox relevance heatmap
% **************************************************************************
% function [comp_hm, rel, pred_class, gray_diff] = compute_lrp_heatmap(or_data, data, im_dim, model, ...
%                           lrp_method, select, shape_labels)
%
% author: Elena Ranguelova, NLeSc
% date created: 30-04-2018
% last modification date: 03-05-2018
% modification details: returns the gray-value difference
% last modification date: 04-06-2018
% modification details: get the shape labels codes as parameter
%**************************************************************************
% INPUTS:
% data          input data of size 1 x image_dimentions_product(after normalization)
% im_dim         image dimentions (original small images) vector
% model         pre-trained model NNet
% lrp_method    method for relevance propagation, one of 3@
%               1 = ratio local and global pre-activtatons (Eq(56) from paper)
%               2 = Using stabilizer  epsilon: 1 (Eq(58) from paper)
%               3 = LRP: Using alpha-beta rule: 2 (Eq(60) from paper)
% select        vector indicating the selected class of to computer relevance against
% shape_labels  the shape label codes
%**************************************************************************
% OUTPUTS:
% comp_hm      rendered image of an input image and a heatmap (HM) as composite HM
% rel          the relevance at the first level
% pred_class   the predicted class
% gray_diff    the absolute gray-value difference between BG and FG
%**************************************************************************
% NOTES:
%**************************************************************************
% EXAMPLES USAGE:
%
% see demo_lrp_exp_lenet_babyaishapes.m
%**************************************************************************
% REFERENCES:
% paper: DOI: 10.1371/journal.pone.0130140
%**************************************************************************
function [comp_hm, rel1, rel2, rel3, pred_class, gray_diff, pred_scores] = compute_both_lrp_heatmaps(or_data, data, im_dim, ...
    model, lrp_method, shape_labels)

% pass the image trough the pre-trained model
pred_classes = model.forward(data);
[~,index_pred_class] = max(pred_classes);
pred_class = shape_labels(index_pred_class);

% compute the relevance after LRP
switch lrp_method
    case 1
        rel1 = model.lrp([1 0]);
        rel2 = model.lrp([0 1]);
        rel3 = model.lrp(pred_classes);
    case 2
        rel1 = model.lrp([1 0],'epsilon',1.);
        rel2 = model.lrp([0 1],'epsilon',1.);
        rel3 = model.lrp(pred_classes,'epsilon',1.);
    case 3
        rel1 = model.lrp([1 0],'alphabeta',2);
        rel2 = model.lrp([0 1],'alphabeta',2);
        rel3 = model.lrp(pred_classes,'alphabeta',2);
end

% For testing whether the relevance scores sum up to the sum of predictions
% By the theory of LRP, the following should be equal, right?
%disp('The sum of pred_classes and sum of relevance scores (after LRP):')
%disp([sum(pred_classes) sum(sum(rel))])

% PLOTTING HEATMAPS
% reshape the input data to an image
inp_shape = reshape(or_data,im_dim);
% quantify contrast
gray_diff = abs(max(or_data(:)) - min(or_data(:)));
% convert the relevance toan RGB image
shape = render.shape_to_rgb(round(inp_shape*255),3);
%shape = render.digit_to_rgb(inp_shape,3);
shape = permute(shape,[2 1 3]);
%cmap = gray(256);
cmap = jet(255);
hm1 = render.hm_to_rgb(rel1,data,3,[],2, cmap);
hm2 = render.hm_to_rgb(rel2,data,3,[],2, cmap);
hm3 = render.hm_to_rgb(rel3,data,3,[],2, cmap);
comp_hm = render.save_image({shape,hm1,hm2,hm3},'../heatmap.png');
pred_scores = pred_classes;
delete('../heatmap.png');






