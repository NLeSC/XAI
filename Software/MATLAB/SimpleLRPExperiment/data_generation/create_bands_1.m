% create_bands_1.m - generating bands around edge of triangle and square shape
n = 32

%  Load the correct class and theta

load('Theta.dat');  load('Class.dat'); 
% Construct either square or triangle: 

r = 0.8* (n/2); 

N = 100000
Bands = zeros(N,n^2);
r_inner = 0.6*(n/2);
r_outer = n/2;

for counter = 1:N
    if rem(counter,1000)==0, counter, end; 
    
    %  Create random angle for first vertex; 
    %  retrieve random angle: 
    theta = Theta(counter);
    class = Class(counter);
    
    if class == 2  %rand<0.5   %  triangle
        Th = zeros(3,1);
        for q = 1:3, Th(q) = theta + (q-1)*2*pi/3; end
    elseif class == 0 %  square
        Th = zeros(4,1);
        for q = 1:4, Th(q) = theta + (q-1)*2*pi/4; end
    end
    
    nr_vertices = length(Th);
    
    Outer = n/2*ones(nr_vertices,2) + r_outer * [cos(Th) sin(Th)];
    Inner = n/2*ones(nr_vertices,2) + r_inner * [cos(Th) sin(Th)];
    
    Outer = round(Outer);   Inner = round(Inner);
     
    %  Compute convex hull and area
    [K, A_outer] = convhull(Outer(:,1),Outer(:,2));
    [K, A_inner] = convhull(Inner(:,1),Inner(:,2));
    
    Polygon_outer = 2*ones(n,n);
    Polygon_inner = ones(n,n);
    
    
    for i = 1:n
        for j = 1:n
            V_outer = [Outer; i j];
            [~,A] = convhull(V_outer(:,1),V_outer(:,2));
            if A>A_outer, Polygon_outer(i,j) = 0; end   %  this is background
            V_inner = [Inner; i j];
            [~,A] = convhull(V_inner(:,1),V_inner(:,2));
            if A>A_inner, Polygon_inner(i,j) = 0; end   %  this is background
        end
    end
    
    %figure(1), imagesc(Polygon)
    
F = [0 1 0; 1 0 1; 0 1 0];

P1 = conv2(Polygon_inner, F,'same');

Polygon_inner_final = Polygon_inner.*(P1>1);
    
    Band = (Polygon_outer == 2).*(Polygon_inner_final ~= 1);
    %Band = bwfill(Band_0,'holes',4);
    
%     figure(1), imagesc(Band)
%     title(int2str(class))
%     %figure(2), imagesc(Band)   
%    pause
    %
% figure(30), 
% subplot(1,2,1), imshow(Polygon)
% subplot(1,2,2), imshow(Polygon_final)
% pause

Bands(counter,:) = Band(:)';

end

csvwrite('Bands.dat',Bands)
% csvwrite('Polygons.dat',P);
% csvwrite('Class.dat',C);
% csvwrite('Theta.dat',Theta)


