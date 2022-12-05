"""
This script will be used to create dataset according yo YOLO v5 sructure from
`SKU-110K_fixed`  

The resulting directory structure should look like this:
    |data/
    |── images
    |   |── train
    |   |   |── train_0.jpg
    |   |   |── train_1.jpg
    |   |   |── train_2.jpg
    |   |   |── ...
    |   |── val
    |   |   |── val_0.jpg
    |   |   |── val_1.jpg
    |   |   |── val_2.jpg
    |   |   |── ...
    |   |── test
    |   |   |── test_0.jpg
    |   |   |── test_1.jpg
    |   |   |── test_2.jpg
    |   |   |── ...
    |── labels
    |   |── train
    |   |   |── train_0.txt
    |   |   |── train_1.txt
    |   |   |── train_2.txt
    |   |   |── ...
    |   |── val
    |   |   |── val_0.txt
    |   |   |── val_1.txt
    |   |   |── val_2.txt
    |   |   |── ...
    |   |── test
    |   |   |── test_0.txt
    |   |   |── test_1.txt
    |   |   |── test_2.txt
    |   |   |── ...
"""
import argparse
import os
import pandas as pd
import numpy as np
import yaml

IMAGES_PATH = '/home/app/src/data/SKU-110K_fixed/images/'
ANNOTATIONS_PATH = '/home/app/src/data/SKU-110K_fixed/annotations/'
OUTPUT_PATH = '/home/app/src/data/'
COLUMNS = ['img_name','xi','yi','xf','yf','label','w','h']

def parse_args():
    parser = argparse.ArgumentParser(description="Train your model.")
    parser.add_argument(
        "--data_folder",
        type=str,
        default=IMAGES_PATH,
        help=(
            "Full path to the directory having all the cars images. E.g. "
            "`/home/app/src/data/car_ims/`."
        ),
    )
    parser.add_argument(
        "--labels",
        type=str,
        default=ANNOTATIONS_PATH,
        help=(
            "Full path to the CSV file with data labels. E.g. "
            "`/home/app/src/data/car_dataset_labels.csv`."
        ),
    )
    parser.add_argument(
        "--output_data_folder",
        type=str,
        default=OUTPUT_PATH,
        help=(
            "Full path to the directory in which we will store the resulting "
            "train/test splits. E.g. `/home/app/src/data/car_ims_v1/`."
        ),
    )

    args = parser.parse_args()

    return args


def main(data_folder, labels, output_data_folder):
    """
    Create images and labels structure for a givin annotation set
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
    annotations_df = pd.read_csv(os.path.join(labels), header=None)
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
    for image_name in images_list:
      image_annotation_df = annotations_df[annotations_df['img_name']==image_name][['class', 'cx', 'cy', 'wb', 'hb']].copy()
      np.savetxt(os.path.join(output_data_folder, 'labels', typeset, os.path.splitext(image_name)[0]+'.txt'), image_annotation_df[['class','cx', 'cy', 'wb', 'hb']].values, ['%i', '%1.4f','%1.4f','%1.4f','%1.4f'])
      os.link(os.path.join(data_folder, image_name),os.path.join(output_data_folder, 'images', typeset, image_name))
    

if __name__ == "__main__":
    args = parse_args()
    # Iterate over all .csv files in labels path
    for annotation_file in os.listdir(args.labels):
      if os.path.splitext(annotation_file)[-1].lower() == '.csv':
        typeset = os.path.splitext(annotation_file)[0].split("_")[1]
        # Create 'images/typeset' and 'labels/typeset' folders in case they do not exist
        if not os.path.isdir(os.path.join(args.output_data_folder,'images', typeset)):
          os.makedirs(os.path.join(args.output_data_folder,'images', typeset))
        if not os.path.isdir(os.path.join(args.output_data_folder,'labels', typeset)):
          os.makedirs(os.path.join(args.output_data_folder,'labels', typeset))
        # Create structure for a given set (train, val or test)
        main(args.data_folder, os.path.join(args.labels, annotation_file), args.output_data_folder)

    # config_dict = {'path': '../data', 'train': 'images/train', 'val':'images/val', 'test':'images/test', 'nc': 1, 'names':["object"]}
    # with open(os.path.join(args.output_data_folder, 'config.yaml'), 'w') as file:
    #   yaml.dump(config_dict, file)