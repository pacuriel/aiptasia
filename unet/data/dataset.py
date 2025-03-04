import os
import matplotlib.pyplot as plt
from torch.utils.data import Dataset
import torchvision.transforms.functional as TF
import cv2
import numpy as np

#class representing the data that inherits from torch.utils.data.Dataset
class ImageDataset(Dataset):
    def __init__(self, image_dir: str, mask_dir: str, transform=None, target_transform=None):
        """
        Input: 
        - image_dir (string): directory with images
        - mask_dir (string): directory with masks
        - transform: transformations to apply to images and masks
        """
        if not (isinstance(image_dir, str) or isinstance(mask_dir, str)): #confirming directory names are strings
            raise TypeError

        ###Consider what transforms we want to do to both the raw image and the target (mask)?
        self.image_dir = image_dir #image directory
        self.mask_dir = mask_dir #mask directory
        self.transform = transform #transformations to apply to input
        self.target_transform = target_transform #transformations to apply to GT masks
        self.image_files = sorted(os.listdir(self.image_dir)) #list of file names
        self.mask_files = sorted(os.listdir(mask_dir))
    #returns size of dataset
    def __len__(self):
        return len(self.image_files)
    
    #used to get a single item given an index
    def __getitem__(self, index):

        image_file = self.image_files[index] # Image file (likely input to model)

        # print(image_file)

        #storing/image/mask path
        image_path = os.path.join(self.image_dir, self.image_files[index])
        # mask_path = os.path.join(self.mask_dir, self.mask_files[index])
        
        #reading in image
        image = cv2.imread(image_path)
        if image is not None: #sanity check bc i had a corrupted image :(
            image = TF.to_tensor(image)
        else: 
            print(f"Image w/ index {index} returned None!")
            print(f"Image path: {image_path}")
            # print(f"Mask path: {mask_path}")
            raise TypeError(f"Image with index {index} and path {image_path} returned with type {type(image)}!")

        # Getting correspoinding mask
        mask = self.__get_correspoding_mask__(image_file)

        # Note: below function converts values from discreet to continuous ([0, 255] -> [0,1])
        mask = TF.to_tensor(mask) # Converting mask to tensor ### Should I do this in the above function call??

        #reading in mask and processing for single channel gray-scale 
        # mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
        # #converting mask to binary (i.e. 0/1)
        # (thresh, mask) = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        # # mask[mask == 255] = 1.0 #TF.to_tensor (below) rescales values from discrete to continuous
        # mask = TF.to_tensor(mask) #converting mask to tensor

        #applying transformations (converting to tensor, etc.)
        if self.transform:
            image = self.transform(image)
        if self.target_transform:
            mask = self.target_transform(mask)
        
        return image, mask, index
    
    def __get_correspoding_mask__(self, image_file: str):
        """Matches input-output files (due to data augmentations)

        Args:
            image_file: The image filename string to be used as input to the model

        Returns: 
            String of corresponding GT mask file (output of model)
            Tensor of corresponding GT mask
        """
        aug_types = ["h", "v", "hv"] # Non-blurred augmentation flags

        mask_file = image_file # Initializing to image file

        # Looping over augmentation types
        for aug in aug_types: 
            if aug in image_file:
                mask_file = image_file
                # Removing blur flag from file
                if "b" in mask_file: 
                    mask_file = mask_file.replace("b", "") # Removing blur flag
        
                # print(mask_file)
                
        # Checking if input is only blur image (no flips)
        if "_b" in image_file:
            mask_file = image_file.replace("_b", "_h") # Replacing blur flag w/ h-flip flag

            mask_path = os.path.join(self.mask_dir, mask_file) # Full path to mask file

            # Reading in mask and processing for single channel gray-scale 
            mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)
            mask = cv2.flip(mask, 1) # Undoing h-flip

            #converting mask to binary (i.e. 0/1)
            (thresh, mask) = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            # mask[mask == 255] = 1.0 #TF.to_tensor (below) rescales values from discrete to continuous
        else: 
            # print(mask_file, self.mask_dir)
            #Load in corresponding mask
            mask_path = os.path.join(self.mask_dir, mask_file) # Full path to mask file

            # Reading in mask and processing for single channel gray-scale 
            mask = cv2.imread(mask_path, cv2.IMREAD_GRAYSCALE)

            #converting mask to binary (i.e. 0/1)
            (thresh, mask) = cv2.threshold(mask, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
            # # mask[mask == 255] = 1.0 #TF.to_tensor (below) rescales values from discrete to continuous

        # print(image_file, mask_file)
        return mask