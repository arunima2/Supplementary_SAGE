from PIL import Image
from scipy import misc
import argparse

ap = argparse.ArgumentParser()
ap.add_argument("-i", "--imagePath", required=True,help="Input image")
#ap.add_argument("-o", "--outPath", required=True,help="Output image")
args = vars(ap.parse_args())
in1 = args['imagePath']
out1 = in1+".out.png"
arr = misc.imread(in1)
arr[arr==2] = 0
arr[arr==3] = 0
f = 255.0
imgg = f*(arr-0)/(1-0)
img = Image.fromarray(imgg)
img.convert('RGB').save(out1)