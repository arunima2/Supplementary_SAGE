#!/bin/bash
DIR1=$1
cd $DIR1
mkdir "ROIs"
mkdir "NonROIs"
for f in *_heatmap.png
do
  #echo "Processing $f file..."
  # take action on each file. $f store current file name
  #cat $f
  fn=$(echo $f | awk -F heatmap.png '{print $1}')
  fn_o=$(echo "$fn"original.png)
  fn_m=$(echo "$fn"heatmap.png)
  fn_r=$(echo "$fn"roi.png)
  fn_r2=$(echo "$fn"roi2.png)
  fn_nr=$(echo "$fn"nonroi.png)
  fn_nr2=$(echo "$fn"nonroi2.png)
  convert -monochrome $fn_m del_mask.png
  convert $fn_m -threshold 60% del_mask2.png
  convert del_mask.png -negate del_mask_negate.png
  convert del_mask2.png -negate del_mask_negate2.png
  convert $fn_o -compose CopyOpacity del_mask_negate.png -alpha Off -composite -trim +repage del_out_temp.png
  convert $fn_o -compose CopyOpacity del_mask_negate2.png -alpha Off -composite -trim +repage del_out_temp2.png
  convert $fn_o -compose CopyOpacity del_mask.png -alpha Off -composite -trim +repage del_out_temp_non.png
  convert $fn_o -compose CopyOpacity del_mask2.png -alpha Off -composite -trim +repage del_out_temp_non2.png
  convert del_out_temp.png -resize 600 $fn_r
  convert del_out_temp2.png -resize 600 $fn_r2
  convert del_out_temp_non.png -resize 600 $fn_nr
  convert del_out_temp_non2.png -resize 600 $fn_nr2
  rm del_mask_negate.png del_mask.png del_mask_negate2.png del_mask2.png del_out_temp.png del_out_temp2.png del_out_temp_non.png del_out_temp_non2.png
  mv $fn_r "ROIs/"
  mv $fn_r2 "ROIs/"
  mv $fn_nr "NonROIs/"
  mv $fn_nr2 "NonROIs/"
done
python ../find_closest_color_python3.py -i ROIs/
python ../find_closest_color_python3.py -i NonROIs/
cd ..
