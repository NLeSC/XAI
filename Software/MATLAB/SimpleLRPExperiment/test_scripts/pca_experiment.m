% after runnig demo_lrp_exp_nn_tri_sq_rot_with_both_selected.m
% run this script for a principle component analysis (PCA).

% we focused on
% 1024_to_8_to_2_short_relu_gray_triangles_and_squares_rotation model here.

% init
W = net.modules{1,1}.W;
B = net.modules{1,1}.B;

% select data for the principle component analysis (PCA)
numb_data = 500;
data_PCA = [squares(1:numb_data, :); triangles(1:numb_data, :)];

% prepare data
PCA_input = data_PCA*W;

% PCA
[coef, scores, L] = pca(PCA_input);

% scores = PCA_input;
% scores = scores + randn(size(scores))/10;

% plot results PCA

figure(10001)
plot(L)
title('L Values')
hold off

figure(10002) 
title('PCA: red are squares and blue are triangles')
plot3(scores(1:numb_data,1), scores(1:numb_data,2), scores(1:numb_data,3),'r.')  % squares
hold on
plot3(scores(numb_data+1:end,1), scores(numb_data+1:end,2), scores(numb_data+1:end,3),'b.')  % triangles
hold off