Image = imread('semicircle.PNG');
subplot(2,3,1)
imshow(Image)
title('Original Image')
subplot(2,3,3)
 cform = makecform('srgb2lab');
lab_he = applycform(Image,cform);
ab = double(lab_he(:,:,2:3));
nrows = size(ab,1);
ncols = size(ab,2);
ab = reshape(ab,nrows*ncols,2);

nColors = 3;
% repeat the clustering 3 times to avoid local minima
[cluster_idx, cluster_center] = kmeans(ab,nColors,'distance','sqEuclidean', ...
                                      'Replicates',3);
                                  
                                  pixel_labels = reshape(cluster_idx,nrows,ncols);
imshow(pixel_labels,[]), title('Image Labeled by Cluster Index');

segmented_images = cell(1,3);
rgb_label = repmat(pixel_labels,[1 1 3]);

for k = 1:nColors
    color = Image;
    color(rgb_label ~= k) = 0;
    segmented_images{k} = color;
end
subplot(2,3,4)
imshow(segmented_images{1}), title('Background-c1');
subplot(2,3,5)
imshow(segmented_images{2}), title('Shape-c2');
subplot(2,3,6)
imshow(segmented_images{3}), title('Letter-c3');

shapeimage=segmented_images{2};
characterimage=segmented_images{3};



