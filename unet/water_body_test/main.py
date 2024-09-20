"""
Main file to test original U-Net model on water body dataset
Pablo A. Curiel
September 2024
"""
import platform
import os

from unet_OG import UNet #importing OG U-Net Model

def main(): 
    if platform.system() == "Linux":
        image_dir = "/home/pcuriel/data/aiptasia/image_data/water_body_data/Images"
        mask_dir = "/home/pcuriel/data/aiptasia/image_data/water_body_data/Masks"

    

if __name__ == "__main__": 
    main()