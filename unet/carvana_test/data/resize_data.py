"""
This file is used to obtain square versions of the water body data. 
Pablo A. Curiel
September 2024
"""
import os
import cv2
from tqdm import tqdm 

from utils import resizeImage, makeImageSquare

if __name__ == "__main__":
    #data directories
    image_dir = "C:\\Users\\giant\\Desktop\\aiptasia\\data\\water_body_data\\Images"
    mask_dir = "C:\\Users\\giant\\Desktop\\aiptasia\\data\\water_body_data\\Masks"

    unet_input_size = 512 #size to make images

    #storing and creating resized directories 
    image_resize_dir = image_dir + "_" + str(unet_input_size)
    mask_resize_dir = mask_dir + "_" + str(unet_input_size)
    os.makedirs(name=(image_dir + "_" + str(unet_input_size)), exist_ok=True) 
    os.makedirs(name=(mask_dir + "_" + str(unet_input_size)), exist_ok=True)

    file_names = sorted(os.listdir(image_dir)) #list of file names

    #looping over files
    for file in tqdm(file_names): 
        #skipping file if already processed
        if file in os.listdir(image_resize_dir) and file in os.listdir(mask_resize_dir):
            continue

        # breakpoint()

        #reading image/mask
        img = cv2.imread(os.path.join(image_dir, file)) 
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB) #converting to RGB
        mask = cv2.imread(os.path.join(mask_dir, file))
        # mask = cv2.cvtColor(mask, cv2.COLOR_BGR2RGB) #converting to RGB
    
        #resizing longest side
        img = resizeImage(img=img, size=unet_input_size)
        mask = resizeImage(img=mask, size=unet_input_size)

        #squaring image/mask
        img = makeImageSquare(img=img, size=unet_input_size)
        mask = makeImageSquare(img=mask, size=unet_input_size)

        #saving resized image/mask
        cv2.imwrite(filename=os.path.join(image_resize_dir, file), img=img) #saving img
        cv2.imwrite(filename=os.path.join(mask_resize_dir, file), img=mask) #saving mask
