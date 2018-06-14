% test_sum_pixel_evidence_2class.m -computing accumulated evidence for
% selected class

%% parameters
config_params_tri_sq;

verbose = true;

%% data loading
% load MAT files with data
load(test_labels_full_fname);
num_test_images = size(test_labels,1);
if verbose
    disp(['Loaded ', num2str(num_test_images) ,' test labels']);
end
num_labels = length(shape_labels);

% load relevance matricies
for s = 1:num_labels
    selected_class = shape_labels(s);
    switch s
        case 1
            select_label = 'square';
        case 2
            select_label = 'triangle';
    end
    relevance_fullfname = fullfile(path2experiments,...
       [relevance_fname_base '_selected_' select_label '.mat']);
    load(relevance_fullfname);    
    switch s
        case 1
            matrix1 = rel_matrix;
        case 2
            matrix2 = rel_matrix;
    end
end

%% compute the evidence
[evidence_same, evidence_diff] = sum_pixels_evidence_2class(test_labels, ...
                          matrix1, matrix2, eps);
                      
if verbose
    disp(['Computed evidence matricies for ', num2str(num_test_images) ,' images.']);
end

if save_evidence
        save(evidence_fullfname, "evidence_same", "evidence_diff");
    if verbose
        disp(['Saved evidence matricies for ', num2str(num_test_images) ,' images.']);
    end
end
