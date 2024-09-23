import os
import torch
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from torch.utils.data import Dataset, DataLoader
from torchvision import transforms, utils
import cv2

#class representing the water body data that inherits from torch.utils.data.Dataset
class WaterBodyDataset(Dataset):
    def __init__(self, image_dir: str, mask_dir: str, transform=None):
        """
        Input: 
        - image_dir (string): directory with images
        - mask_dir (string): directory with masks
        - transform: transformations to apply to images and masks
        """
        self.image_dir = image_dir
        self.mask_dir = mask_dir
        self.transform = transform
        self.file_names = sorted(os.listdir(self.image_dir))

    #returns size of dataset
    def __len__(self):
        return len(self.file_names)
    
    #used to get a single item given an index
    def __getitem__(self, index):
        #storing/image/mask path
        image_path = os.path.join(self.image_dir, self.file_names[index])
        mask_path = os.path.join(self.mask_dir, self.file_names[index])
        
        #storing image/mask
        image = cv2.imread(image_path) 
        mask = cv2.imread(mask_path)

        #applying transformations (if any)
        if self.transform:
            image, mask = self.transform(image, mask)
        
        return image, mask

