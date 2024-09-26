from PIL import Image
from pathlib import Path
import matplotlib.pyplot as plt
import platform
import os
import numpy as np
import random
import cv2

import torch
# from torchvision.transforms import v2
import torchvision.transforms as T
import glob

if __name__ == "__main__":
    #getting directories with data
    if platform.system() == "Linux":
        image_dir = "/home/pcuriel/data/aiptasia/image_data/kaden_data/2023.12.8"
    
    files = glob.glob(image_dir + "/*.png")

    print(files)
    exit()

    test_img_name = os.listdir(image_dir)[img_idx] #file path of test image


    """Practicing tiling images"""
    img = cv2.imread(os.path.join(image_dir, test_img_name))
    print(type(img))
    unet_input_size = 572 #square images
    
    

    breakpoint()