""" 
Original Author  Ernesto P. Adorio, Ph.D 
Original Source: http://my-other-life-as-programmer.blogspot.com/2012/02/python-finding-nearest-matching-color.html
Modifed By: JDiscar
Further Modified By: arunima2
This class maps an RGB value to the nearest color name it can find. Code is modified to include 
ImageMagick names and WebColor names.  
1. Modify the minimization criterion to use least sum of squares of the differences.
2. Provide error checking for input R, G, B values to be within the interval [0, 255].
3. Provide different ways to specify the input RGB values, aside from the (R, G, B) values as done in the program above.
"""

import cv2
import numpy as np
import argparse
#from utils.colorutils import get_dominant_color
import PIL
import colorsys
from matplotlib.colors import hsv_to_rgb
import os
from sklearn.cluster import KMeans
from collections import Counter

class ColorNames:
    
    WebColorMap = {}
    WebColorMap["Purple"] = "#4B0082"
    WebColorMap["Pink"] = "#DA70D6"
    WebColorMap["White"] = "#FFFFFF"
    
    
    # src: http://www.imagemagick.org/script/color.php
    ImageMagickColorMap = {}
    ImageMagickColorMap["snow"] = "#FFFAFA"
    ImageMagickColorMap["snow1"] = "#FFFAFA"
    ImageMagickColorMap["snow2"] = "#EEE9E9"
    
    @staticmethod
    def rgbFromStr(s):  
        # s starts with a #.  
        r, g, b = int(s[1:3],16), int(s[3:5], 16),int(s[5:7], 16)  
        return r, g, b  
    
    @staticmethod
    def findNearestWebColorName(R,G,B):  
        return ColorNames.findNearestColorName(R,G,B,ColorNames.WebColorMap)
    
    @staticmethod
    def findNearestColorName(R,G,B,Map):  
        mindiff = None
        for d in Map:  
            r, g, b = ColorNames.rgbFromStr(Map[d])  
            diff = abs(R -r)*256 + abs(G-g)* 256 + abs(B- b)* 256   
            if mindiff is None or diff < mindiff:  
                mindiff = diff  
                mincolorname = d  
        return mincolorname   


def hsv2rgb(hsv):
    return hsv_to_rgb(hsv)
    
def get_dominant_color(image, k=4, image_processing_size = None):
	"""
	takes an image as input and returns the dominant color in the image as a list
	
	dominant color is found by performing k means on the pixel colors and returning the centroid
	of the largest cluster

	processing time is sped up by working with a smaller image; this can be done with the 
	image_processing_size param which takes a tuple of image dims as input

	>>> get_dominant_color(my_image, k=4, image_processing_size = (25, 25))
	[56.2423442, 34.0834233, 70.1234123]
	"""
	#resize image if new dims provided
	if image_processing_size is not None:
		image = cv2.resize(image, image_processing_size, interpolation = cv2.INTER_AREA)
	
	#reshape the image to be a list of pixels
	image = image.reshape((image.shape[0] * image.shape[1], 3))

	#cluster the pixels and assign labels
	clt = KMeans(n_init=10, n_clusters = k)
	labels = clt.fit_predict(image)

	#count labels to find most popular
	label_counts = Counter(labels)

	#subset out most popular centroid
	dominant_color = clt.cluster_centers_[label_counts.most_common(1)[0][0]]

	return list(dominant_color)

       
  
if __name__ == "__main__":             
	ap = argparse.ArgumentParser()
	ap.add_argument("-i", "--imagePath", required=True,help="Path to image to find dominant color of")
	ap.add_argument("-k", "--clusters", default=4, type=int,help="Number of clusters to use in kmeans when finding dominant color")
	args = vars(ap.parse_args())
	for filename in os.listdir(args['imagePath']):
		if filename.endswith(".png"):
			bgr_image = cv2.imread(os.path.join(args['imagePath'], filename))
			#convert to HSV; this is a better representation of how we see color
			hsv_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2HSV)
			dom_color = get_dominant_color(hsv_image, k=args['clusters'])
			#create a square showing dominant color of equal size to input image
			dom_color_hsv = np.full(bgr_image.shape, dom_color, dtype='uint8')
			#convert to bgr color space for display
			dom_color_bgr = cv2.cvtColor(dom_color_hsv, cv2.COLOR_HSV2BGR)
			output_image = np.hstack((bgr_image, dom_color_bgr))
			r1,g1,b1 = dom_color_bgr[1,1]
			print(filename+","+ColorNames.findNearestWebColorName(r1,g1,b1))
			#print ColorNames.findNearestWebColorName(dom_color_bgr[1,1])
		else:
			continue