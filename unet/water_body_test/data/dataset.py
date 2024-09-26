import os
import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
import torchvision.transforms.functional as TF
import cv2

#class representing the water body data that inherits from torch.utils.data.Dataset
class WaterBodyDataset(Dataset):
    def __init__(self, image_dir: str, mask_dir: str, transform=None, target_transform=None):
        """
        Input: 
        - image_dir (string): directory with images
        - mask_dir (string): directory with masks
        - transform: transformations to apply to images and masks
        """
        ###Consider what transforms we want to do to both the raw image and the target (mask)?
        self.image_dir = image_dir #image directory
        self.mask_dir = mask_dir #mask directory
        self.transform = transform #transformations to apply to input
        self.target_transform = target_transform #transformations to apply to GT masks
        self.file_names = sorted(os.listdir(self.image_dir)) #list of file names

    #returns size of dataset
    def __len__(self):
        return len(self.file_names)
    
    #used to get a single item given an index
    def __getitem__(self, index):
        #storing/image/mask path
        image_path = os.path.join(self.image_dir, self.file_names[index])
        mask_path = os.path.join(self.mask_dir, self.file_names[index])
        
        #reading in image
        image = cv2.imread(image_path)
        image = TF.to_tensor(pic=image)

        #reading in mask and processing for single channel gray-scale 
        mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        
        #converting mask to binary 0-1
        (thresh, mask) = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        mask[mask == 255] = 0 

        #applying transformations (converting to tensor, etc.)
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            mask = self.target_transform(mask)
        
        return image, mask
    