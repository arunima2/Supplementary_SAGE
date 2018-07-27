
#!/bin/bash

## Set up environment which can run CellProfiler and ilastik here
path_to_ilastik=$1
DIR_D=$2 #$(dirname "${roi}")
prefix=$3
DIR_H="."
for f1 in $DIR_D/*roi2.png
do
	$path_to_ilastik/run_ilastik.sh --headless --project $DIR_H/Classify_Cells_osc.ilp  --export_source="Simple Segmentation" $f1
done
cd $DIR_D
rename ' ' '_' *Segmentation.png
cd $DIR_H
for f2 in $DIR_D/*_Simple_Segmentation.png
do
        python label_to_cells.py -i $f2 
done

cd $DIR_D
mkdir cellin_ss
mkdir cellout_ss
mkdir cellin_tx
mkdir cellout_tx
mv *.out.png cellin_ss/
mv *roi2.png cellin_tx/
cd $DIR_H
cellprofiler -p $DIR_H/SizeShape_pipeline.cppipe -c -i $DIR_D/cellin_ss -o $DIR_D/cellout_ss
cellprofiler -p $DIR_H/Texture_pipeline.cppipe -c -i $DIR_D/cellin_tx -o $DIR_D/cellout_tx
cd $DIR_D/cellout_ss
rename 'SizeShape' "SizeShape_${prefix}" *
cd $DIR_D/cellout_tx
rename 'Texture' "Texture_${prefix}" *
