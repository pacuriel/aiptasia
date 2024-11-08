import os
import itertools    
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
from natsort import natsorted
from tqdm import tqdm

from utils import *

TILE_SIZE = 512

def main():
    
    """
    Stitching pred mask back to full images
    """
    pred_mask_tile_dir = "/home/pcuriel/data/aiptasia/code/unet/carvana_test/experiments/04-Nov-2024_1605_03/mask_arrays"    
    pred_mask_tile_files = natsorted(os.listdir(pred_mask_tile_dir))
    pred_img_dir = "/home/pcuriel/data/aiptasia/code/unet/carvana_test/experiments/04-Nov-2024_1605_03/mask_images"
    os.makedirs(pred_img_dir, exist_ok=True)

    gt_mask_dir = "/home/pcuriel/data/aiptasia/image_data/carvana_data/full_dataset/test_masks"
    gt_mask_files = natsorted(os.listdir(gt_mask_dir))
    gt_img_dir = "/home/pcuriel/data/aiptasia/image_data/carvana_data/full_dataset/test_masks" #note: .gif (bc of fucking course it is)
    
    gt_mask = np.array(Image.open(os.path.join(gt_mask_dir, gt_mask_files[0])).convert("L"), dtype=np.uint8)
    (thresh, gt_mask) = cv2.threshold(gt_mask, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    gt_mask[gt_mask == 255] = 1.0
    padded_gt_mask = padImage(img=gt_mask, tile_size=TILE_SIZE)

    num_tiles_per_image = 12

    file_iter = enumerate(tqdm(pred_mask_tile_files))

    for i, pred_mask_file in file_iter:
        #skipping if already processed
        # if (pred_basename + ".png") in os.listdir(pred_img_dir):
        #     continue

        tiles = []

        tile_idx = 0

        pred_basename = pred_mask_file.split(".")[0][:-2]
        # print(pred_basename) #sanity check

        #while loop to get list of tiles
        while len(tiles) < num_tiles_per_image:
            tile = np.load(file=os.path.join(pred_mask_tile_dir, pred_mask_file))
            tiles.append(tile)
    
            if len(tiles) < num_tiles_per_image:
                i, pred_mask_file = next(file_iter)
    
            tile_idx += 1 #incrementing index
        #stitching tiles together
        padded_pred_mask = stitchTiles(tiles=tiles, img_shape=padded_gt_mask.shape)

        #unpadding image back to original size
        pred_mask = unpadImage(img=padded_pred_mask, img_shape=gt_mask.shape, tile_size=TILE_SIZE)

        #saving predicted mask
        # plt.imshow(pred_mask, cmap="binary_r")
        # plt.savefig(os.path.join(pred_img_dir, pred_basename + ".png"))
        cv2.imwrite(os.path.join(pred_img_dir, pred_basename + ".png"), pred_mask*255)

if __name__ == "__main__":
    main()