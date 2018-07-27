Color based analysis of CNN-ROIs

#####Usage##############
./Get_important_regions_usable.sh Test_folder/
########################

Utilized and builds on code from:
(1) https://gist.github.com/jdiscar/9144764
(2) https://github.com/AdamSpannbauer/iphone_app_icon
(3) http://my-other-life-as-programmer.blogspot.com/2012/02/python-finding-nearest-matching-color.html

Separates out ROI and NonROI regions and processes them separately to gauge the dominant color in these regions.

Uses: Imagemagick and the required python libraries as listed within the code.
Folder must contain original file and the vizmask generated from Class Activation Mapping