import os
import itertools    
import numpy as np
import matplotlib.pyplot as plt
import cv2
from PIL import Image
from natsort import natsorted
from tqdm import tqdm
import seaborn as sns

from utils import *

TILE_SIZE = 256

def main():
    
    """
    Stitching pred mask tiles back to full image
    """
    
    # pred_mask_tile_dir = "/home/pcuriel/data/aiptasia/code/unet/carvana_test/experiments/04-Nov-2024_1605_03/mask_arrays"    
    pred_mask_tile_dir = "/home/pcuriel/data/aiptasia/code/unet/experiments/04-Mar-2025_1104_09/mask_arrays"    
    pred_mask_tile_files = natsorted(os.listdir(pred_mask_tile_dir))

    # Converting mask array to mask image
    

    # pred_img_dir = "/home/pcuriel/data/aiptasia/code/unet/carvana_test/experiments/04-Nov-2024_1605_03/mask_images"
    pred_img_dir = "/home/pcuriel/data/aiptasia/code/unet/experiments/04-Mar-2025_1104_09/mask_images"    
    # pred_img_dir = "/home/pcuriel/data/aiptasia/code/unet/carvana_test/experiments/04-Nov-2024_1605_03/heatmaps"
    os.makedirs(pred_img_dir, exist_ok=True)

    # gt_mask_dir = "/home/pcuriel/data/aiptasia/image_data/carvana_data/full_dataset/test_masks"
    gt_mask_dir = "/home/pcuriel/data/aiptasia/image_data/steve_data/test_masks"
    gt_mask_files = natsorted(os.listdir(gt_mask_dir))
    # gt_img_dir = "/home/pcuriel/data/aiptasia/image_data/carvana_data/full_dataset/test_masks" #note: .gif (bc of fucking course it is)
    
    gt_mask = np.array(Image.open(os.path.join(gt_mask_dir, gt_mask_files[0])).convert("L"), dtype=np.uint8)
    (thresh, gt_mask) = cv2.threshold(gt_mask, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    gt_mask[gt_mask == 255] = 1.0
    padded_gt_mask = padImage(img=gt_mask, tile_size=TILE_SIZE)
    num_tiles_per_image = (padded_gt_mask.shape[0] / TILE_SIZE) * (padded_gt_mask.shape[1] / TILE_SIZE)

    file_iter = enumerate(tqdm(pred_mask_tile_files))
    for i, pred_mask_file in file_iter:
        #skipping if already processed
        # if (pred_basename + ".png") in os.listdir(pred_img_dir):
        #     continue

        tiles = []

        tile_idx = 0

        pred_basename = os.path.splitext(pred_mask_file)[0]
        pred_basename = pred_basename.replace("_0", "")
        # print(pred_basename) #sanity check

        #while loop to get list of tiles
        while len(tiles) < num_tiles_per_image:
            tile = np.load(file=os.path.join(pred_mask_tile_dir, pred_mask_file))
            tiles.append(tile)
    
            if len(tiles) < num_tiles_per_image:
                i, pred_mask_file = next(file_iter)
    
            tile_idx += 1 #incrementing index
        #stitching tiles together
        padded_pred_mask = stitchTiles(tiles=tiles, img_shape=padded_gt_mask.shape, data_type=np.float32)
        
        del(tiles)

        #unpadding image back to original size
        pred_mask = unpadImage(img=padded_pred_mask, img_shape=gt_mask.shape, tile_size=TILE_SIZE, data_type=np.float32)
        
        height, width = pred_mask.shape
        aspect_ratio = width / height
        fig, ax = plt.subplots(figsize=(10, 10 / aspect_ratio))

        # heatmap = sns.heatmap(pred_mask, ax=ax, xticklabels=False, yticklabels=False, cmap="hot", square=False)
        # heatmap.set_title(pred_basename)
        # heatmap.figure.savefig(os.path.join(pred_img_dir, pred_basename + ".png"))
        # plt.close()

        #saving predicted mask
        # plt.imshow(pred_mask, cmap="binary_r")
        # plt.savefig(os.path.join(pred_img_dir, pred_basename + ".png"))
        # breakpoint()
        cv2.imwrite(os.path.join(pred_img_dir, pred_basename + ".png"), pred_mask*255)

if __name__ == "__main__":
    main()