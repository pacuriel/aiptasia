"""
Main file to test original U-Net model on water body dataset
Pablo A. Curiel
September 2024
"""
import platform
import os
import torch.nn as nn
import torch.optim as optim
import torch
from tqdm import tqdm

from unet_OG import UNet #importing OG U-Net Model
from dataset import WaterBodyDataset #dataset class
from train import Train

#setting global variables
device = "cuda" if torch.cuda.is_available() else "cpu" #device for pytorch

###Note: sample initial weigths from a Gaussian distribution w/ std_dev = sqrt(2 / N), where N = # incoming nodes (per last paragraph of section 3) 

def main(): 
    input_size = 572 #size of square image input for U-Net
    ###TODO: find way to account for output size w/o hard-coding
    output_size = 388 #size of output images 

    #storing image and mask directories
    if platform.system() == "Linux":
        root_dir = "/home/pcuriel/data/aiptasia/image_data/water_body_data/"
        image_dir = root_dir + "Images"
        mask_dir = root_dir + "Masks"
        if input_size is not None: 
            image_dir += "_" + str(input_size)
            mask_dir += "_" + str(output_size)
    elif platform.system() == "Windows": 
        root_dir = "C:\\Users\\giant\\Desktop\\aiptasia\\data\\water_body_data"
        image_dir = root_dir + "\\Images"
        mask_dir = root_dir + "\\Masks"
        if input_size is not None: 
            image_dir += "_" + str(input_size)
            mask_dir += "_" + str(output_size)

    model = UNet(in_channels=3, out_channels=2).to(device) #initializing model
    loss = nn.CrossEntropyLoss()
    # optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    dataset = WaterBodyDataset(image_dir=image_dir, mask_dir=mask_dir) #dataset object
    breakpoint()
    for i, (image, mask) in enumerate(dataset):
        print(i, image.shape, mask.shape)
        breakpoint()
        if i == 3: break

    trainer = Train(model=model, loss=loss, dataset=dataset)
    # print(trainer)

if __name__ == "__main__": 
    main()