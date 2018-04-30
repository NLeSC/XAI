% compute_lrp_heatmap - computes LRP toolbox relevance heatmap
% **************************************************************************
% function [comp_hm, rel, pred_class] = compute_lrp_heatmap(data, im_dim, model, ...
%                           lrp_method, select)
%
% author: Elena Ranguelova, NLeSc
% date created: 30-04-2018
% last modification date:
% modification details:
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
%**************************************************************************
% OUTPUTS:
% comp_hm      rendered image of an input image and a heatmap (HM) as composite HM
% rel          the relevance at the first level
% pred_class   the predicted class
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
function [comp_hm, rel, pred_class] = compute_lrp_heatmap(data, im_dim, ...
    model, lrp_method, select)

% pass the image trough the pre-trained model
pred_classes = model.forward(data);
[~,pred_class] = max(pred_classes);

% compute the relevance after LRP
switch lrp_method
    case 1
        rel = model.lrp(select);
    case 2
        rel = model.lrp(select,'epsilon',1.);
    case 3
        rel = model.lrp(select,'alphabeta',2);
end

% reshape the input data to an image
inp_shape = reshape(data,im_dim);
% convert the relevance toan RGB image
shape = render.shape_to_rgb(round(inp_shape*255),3);
shape = permute(shape,[2 1 3]);
hm = render.hm_to_rgb(rel,data,3,[],2);
comp_hm = render.save_image({shape,hm},'../heatmap.png');
delete('../heatmap.png');






