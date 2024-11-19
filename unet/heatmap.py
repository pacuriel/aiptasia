import torch
from torch.utils.data import DataLoader
import matplotlib.pyplot as plt
from tqdm import tqdm 
import os
import numpy as np
from natsort import natsorted

from data import ImageDataset #dataset class
from utils import stitchTiles, unpadImage

TILE_SIZE = 512
batch_size = 16

#loading model
test_model_path = "/home/pcuriel/data/aiptasia/code/unet/carvana_test/experiments/04-Nov-2024_1605_03/best_test_model.pt"
device = "cuda" if torch.cuda.is_available() else "cpu" #device for pytorch
model = torch.load(test_model_path, weights_only=False)
model.to(device)
model.eval()

#data directories
root_dir = "/home/pcuriel/data/aiptasia/image_data/carvana_data/full_dataset/"
test_img_dir = root_dir + "test_images/" + f"tiles_{TILE_SIZE}"
test_mask_dir = root_dir + "test_masks/" + f"tiles_{TILE_SIZE}"
test_files = sorted(os.listdir(test_img_dir))
heatmap_dir = "/home/pcuriel/data/aiptasia/code/unet/carvana_test/experiments/04-Nov-2024_1605_03/heatmaps"

#loading data
test_set = ImageDataset(image_dir=test_img_dir, mask_dir=test_mask_dir)
test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False)

def saveHeatmapTiles(pred_masks, indices) -> None:
    pred_masks = pred_masks.squeeze().cpu().numpy()
    
    for i, mask in enumerate(pred_masks):
        np.save(file=os.path.join(heatmap_dir, "heatmap_tiles", test_files[indices[i]][:-3] + "npy"), arr=mask)

def stitchHeatmapTiles() -> None:
    print("Stitching heatmap tiles")
    heatmap_tile_dir = os.path.join(heatmap_dir, "heatmap_tiles")
    heatmap_tile_files = natsorted(os.listdir(heatmap_tile_dir))

    num_tiles_per_image = 12

    file_iter = enumerate(tqdm(heatmap_tile_files))

    for i, heatmap_tile_file in file_iter:
        tiles = []

        tile_idx = 0

        while(len(tiles)) < num_tiles_per_image:
            tile = np.load(file=os.path.join(heatmap_tile_dir, heatmap_tile_file))
            tiles.append(tile)
    
            if len(tiles) < num_tiles_per_image:
                i, heatmap_tile_file = next(file_iter)
    
            tile_idx += 1 #incrementing index
        
        # #stitching tiles together
        # padded_pred_mask = stitchTiles(tiles=tiles, img_shape=padded_gt_mask.shape)

        # #unpadding image back to original size
        # pred_mask = unpadImage(img=padded_pred_mask, img_shape=gt_mask.shape, tile_size=TILE_SIZE)


def main():
    print("Running through network and saving heatmap tiles")
    
    loop = tqdm(test_loader)

    with torch.no_grad():
        for batch_idx, (img_batch, gt_mask_batch, indices) in enumerate(loop):
            img_batch = img_batch.to(device) #batch of images
            gt_mask_batch = gt_mask_batch.float().to(device) #batch of masks (unsqueeze to add single channel dimension)
            pred_masks = model(img_batch) #forward pass
            pred_masks = torch.sigmoid(pred_masks) #applying sigmoid function (getting between zero and one)

            saveHeatmapTiles(pred_masks, indices)

    # stitchHeatmapTiles()

if __name__ == "__main__":
    main()