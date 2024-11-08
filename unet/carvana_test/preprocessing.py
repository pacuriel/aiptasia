import os
import numpy as np
import cv2
from PIL import Image
from tqdm import tqdm

from utils import tileImage, padImage

#data directories
BASE_DIR = "/home/pcuriel/data/aiptasia/image_data/carvana_data/full_dataset"
TRAIN_IMAGE_DIR = os.path.join(BASE_DIR, "train_images")
TRAIN_MASK_DIR = os.path.join(BASE_DIR, "train_masks")
TEST_IMAGE_DIR = os.path.join(BASE_DIR, "test_images")
TEST_MASK_DIR = os.path.join(BASE_DIR, "test_masks")

#size of tiles to create
TILE_SIZE = 256

#function to tile images into non-overlapping squares of a given size
def preprocess(directories: list[list[str]]) -> None:
    #looping over directories    
    for directory in directories:
        print(directory) #sanity check

        #creating directory to save tiles
        tile_save_dir = f"tiles_{TILE_SIZE}"; tile_save_dir = os.path.join(directory, tile_save_dir) #directory to store tiles
        os.makedirs(tile_save_dir, exist_ok=True)

        #looping over files in current dir
        for file in tqdm(sorted(os.listdir(directory))):
            if file[-3:] == "gif": #mask
                # mask = np.array(Image.open(os.path.join(mask_path, mask_file_name)).convert("L"), dtype=np.float32)
                img = np.array(Image.open(os.path.join(directory, file)).convert("L"), dtype=np.uint8)
                (thresh, img) = cv2.threshold(img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
                img[img == 255] = 1.0
            elif file[-3:] == "jpg": #image
                img = cv2.imread(os.path.join(directory, file))
            else: continue #skipping if neither

            #padding image (if necessary) to avoid overlapping tiles
            img = padImage(img=img, tile_size=TILE_SIZE)

            #tiling image and saving tiles
            tileImage(img=img, tile_size=TILE_SIZE, save_tiles=True, tile_dir=os.path.join(tile_save_dir, file))

def main():
    preprocess([TRAIN_IMAGE_DIR, TRAIN_MASK_DIR, TEST_IMAGE_DIR, TEST_MASK_DIR])

if __name__ == "__main__":
    main()