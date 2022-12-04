"""
This script will be used to separate and copy images coming from
`car_ims.tgz` (extract the .tgz content first) between `train` and `test`
folders according to the column `subset` from `car_dataset_labels.csv`.
It will also create all the needed subfolders inside `train`/`test` in order
to copy each image to the folder corresponding to its class.

The resulting directory structure should look like this:
    data/
    ├── car_dataset_labels.csv
    ├── car_ims
    │   ├── 000001.jpg
    │   ├── 000002.jpg
    │   ├── ...
    ├── car_ims_v1
    │   ├── test
    │   │   ├── AM General Hummer SUV 2000
    │   │   │   ├── 000046.jpg
    │   │   │   ├── 000047.jpg
    │   │   │   ├── ...
    │   │   ├── Acura Integra Type R 2001
    │   │   │   ├── 000450.jpg
    │   │   │   ├── 000451.jpg
    │   │   │   ├── ...
    │   ├── train
    │   │   ├── AM General Hummer SUV 2000
    │   │   │   ├── 000001.jpg
    │   │   │   ├── 000002.jpg
    │   │   │   ├── ...
    │   │   ├── Acura Integra Type R 2001
    │   │   │   ├── 000405.jpg
    │   │   │   ├── 000406.jpg
    │   │   │   ├── ...
"""
import argparse
import os
import pandas as pd
import numpy as np

IMAGES_PATH = '/home/app/src/data/SKU-110K_fixed/images/'
ANNOTATIONS_PATH = '/home/app/src/data/SKU-110K_fixed/annotations/'
COLUMNS = ['img_name','xi','yi','xf','yf','label','w','h']

def parse_args():
    parser = argparse.ArgumentParser(description="Train your model.")
    parser.add_argument(
        "data_folder",
        type=str,
        help=(
            "Full path to the directory having all the cars images. E.g. "
            "`/home/app/src/data/car_ims/`."
        ),
    )
    parser.add_argument(
        "labels",
        type=str,
        help=(
            "Full path to the CSV file with data labels. E.g. "
            "`/home/app/src/data/car_dataset_labels.csv`."
        ),
    )
    parser.add_argument(
        "output_data_folder",
        type=str,
        help=(
            "Full path to the directory in which we will store the resulting "
            "train/test splits. E.g. `/home/app/src/data/car_ims_v1/`."
        ),
    )

    args = parser.parse_args()

    return args


def main(data_folder, labels, output_data_folder):
    """
    Parameters
    ----------
    data_folder : str
        Full path to raw images folder.

    labels : str
        Full path to CSV file with data annotations.

    output_data_folder : str
        Full path to the directory in which we will store the resulting
        train/test splits.
    """
    # Get the type of set, train, val or test
    typeset = os.path.splitext(os.path.basename(labels))[0].split("_")[1]
    # Load labels as a dataframe
    annotations_df = pd.read_csv(os.path.join(ANNOTATIONS_PATH,'annotations_train.csv'), header=None)
    annotations_df.columns = COLUMNS
    # Get list of unique image names
    images_list = annotations_df['img_name'].unique().tolist()
    # Add YOLO formatted columns 
    annotations_df['class'] = 0
    annotations_df['cx'] = (annotations_df['xi'] + annotations_df['xf'])/(2*annotations_df['w'])
    annotations_df['cy'] = (annotations_df['yi'] + annotations_df['yf'])/(2*annotations_df['h'])
    annotations_df['wb'] = (annotations_df['xf'] - annotations_df['xi'])/(annotations_df['w'])
    annotations_df['hb'] = (annotations_df['yf'] - annotations_df['yi'])/(annotations_df['h'])
    # Loop over the images and create dataset (images and labels text files)
    a = 0
    for image_name in images_list:
      image_annotation_df = annotations_df[annotations_df['img_name']==image_name][['class', 'cx', 'cy', 'wb', 'hb']].copy()
      np.savetxt(os.path.join(output_data_folder, 'labels', typeset, os.path.splitext(image_name)[0]+'.txt'), image_annotation_df[['class','cx', 'cy', 'wb', 'hb']].values, ['%i', '%1.4f','%1.4f','%1.4f','%1.4f'])
      os.link(os.path.join(data_folder, image_name),os.path.join(output_data_folder, 'images', typeset, image_name))
      if a>5:
        break
      a = a+1
    


if __name__ == "__main__":
    args = parse_args()
    typeset = os.path.splitext(os.path.basename(args.labels))[0].split("_")[1]
    if not os.path.isdir(os.path.join(args.output_data_folder,'images', typeset)):
      os.makedirs(os.path.join(args.output_data_folder,'images', typeset))
    if not os.path.isdir(os.path.join(args.output_data_folder,'labels', typeset)):
      os.makedirs(os.path.join(args.output_data_folder,'labels', typeset))


    main(args.data_folder, args.labels, args.output_data_folder)
