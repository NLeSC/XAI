% create_shapes_2 - generating triangles and squares dataset
n = 32

% Construct either square or triangle: 

r = 0.8* (n/2); 

N = 100000
P = zeros(N,n^2);
C = zeros(N,1);
Theta = zeros(N,1);   %  angle for first vertex; 

for counter = 1:N
    if rem(counter,1000)==0, counter, end; 
    % define background and fore-ground gray level  (btween 0 and 1)
    gray_bg = rand; 
    gray_fg = rand; 
    
    %  Create random angle for first vertex; 
    theta = 2*pi*rand;
    Theta(counter) = theta; 
    
if rand<0.5   %  triangle
    C(counter) = 2; 
    
    th0 = theta;  th1 =theta+2*pi/3;  th2 = theta+4*pi/3; 
    V0 = [n/2 + r*cos(th0), n/2+r*sin(th0) ;  
        n/2 + r*cos(th1), n/2+r*sin(th1) ;
        n/2 + r*cos(th2), n/2+r*sin(th2)] ;
    V0  = round(V0);
else    %  square
    C(counter) = 0;
    th0 = theta;  th1 =theta+pi/2;  th2 = theta+pi;  th3 = theta+3*pi/2;
    V0 = [n/2 + r*cos(th0), n/2+r*sin(th0) ;  
        n/2 + r*cos(th1), n/2+r*sin(th1) ;
        n/2 + r*cos(th2), n/2+r*sin(th2);
         n/2 + r*cos(th3), n/2+r*sin(th3)] ;
    V0  = round(V0);
end

    

%  Compute convex hull and area
[K, A0] = convhull(V0(:,1),V0(:,2));

Polygon = ones(n,n);

for i = 1:n
    for j = 1:n 
        V = [V0; i j];
        [~,A] = convhull(V(:,1),V(:,2));
        if A>A0, Polygon(i,j) = 0; end   %  this is background
    end 
end

%figure(1), imagesc(Polygon)

F = [0 1 0; 1 0 1; 0 1 0];

P1 = conv2(Polygon, F,'same');

Polygon_final = Polygon.*(P1>1);
Polygon_final = gray_bg*(Polygon_final==0) + gray_fg*(Polygon_final==1);
% 
% figure(30), 
% subplot(1,2,1), imshow(Polygon)
% subplot(1,2,2), imshow(Polygon_final)
% pause

P(counter,:) = Polygon_final(:)';

end

csvwrite('Polygons.dat',P);
csvwrite('Class.dat',C);
csvwrite('Theta.dat',Theta)


