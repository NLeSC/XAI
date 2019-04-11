
%%  Experiment:  create images with a variable number of circles, at variable 
%  locations and of variable size.  IN addition, the contrast between fore-
%  and back ground is also random. 
%  The challenge is to create a neural net that correctly determines the
%  number of foreground objects. 

%  This program creates a matrix P such that each line represent an image
%  

n = 100   % linear dimension of the image 

% Construct either square or triangle: 

% r = 0.8* (n/2); 

N = 30000
P =  uint8(zeros(N,n^2));
C_planned = zeros(N,1);    %  count  planned
C_actual = zeros(N,1);     %  count  actual (objects might overlap; 
Theta = zeros(N,1);   %  angle for first vertex; 

for i = 1: N    %  Cycle over images
    
    if rem(i,500) == 0, i, end
    
    I = zeros(n,n);  
    [X,Y] = meshgrid(1:n);
    
    %  generate intended number of circles; 
    
    c_planned = unidrnd(3);   % random number 1-3 of planned circles
    C_planned(i) = c_planned; 
    
    % Loop over the different objects
    for j = 1:c_planned
        
        %  pick random centre and random radius
        ii = unidrnd(n); jj = unidrnd(n);
        r = 5 + (n/6)*rand;
        
        % Create 
        dI = ((X-ii).^2 + (Y-jj).^2 < r^2);
        I = max(I,dI); 
    end
        
    % Due to overlap, there might be less objects than planned; 
    
    [~,c_actual] = bwlabel(I);
    C_actual(i) = c_actual; 
    
    %  Finally, assign random contrast: 
%     colors_perm = randperm(256);
%     bg_color = colors_perm(1)-1; 
%     fg_color = colors_perm(2)-1; 
%     
    fg_color = rand;  
    bg_color = rand; 
    while abs(bg_color-fg_color) < 0.1
        bg_color = rand;
    end
    
    I_final = fg_color*(I==1) + bg_color*(I==0)+ 0.05*randn(size(I));
    I_final = uint8(round(255*I_final));
    
%     figure(1), imagesc(I_final),colormap(gray)
%     title(['Nr of objects; planned = ' int2str(c_planned) ' actual = ' int2str(c_actual)]  )
%  
    P(i,:) = I_final(:)';
    %pause     
 
end 

save P P
save C_actual C_actual
save C_planned C_planned
