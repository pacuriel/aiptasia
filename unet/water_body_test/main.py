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
from data import WaterBodyDataset #dataset class
from train import Train

RANDOM_SEED = 42 #random seed for testing (not so random i guess?)

#setting global variables
device = "cuda" if torch.cuda.is_available() else "cpu" #device for pytorch

###Note: sample initial weigths from a Gaussian distribution w/ std_dev = sqrt(2 / N), where N = # incoming nodes (per last paragraph of section 3) 

#function to store directories w/ data
def storeDirs(input_size: int, output_size: int) -> tuple[str, str]:
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

    return image_dir, mask_dir

def main(): 
    input_size = 572 #size of square image input for U-Net
    ###TODO: find way to account for output size w/o hard-coding
    output_size = 388 #size of output images

    image_dir, mask_dir = storeDirs(input_size, output_size)
    num_samples = len(os.listdir(image_dir))

    #TODO: determine what transforms to apply
    dataset = WaterBodyDataset(image_dir=image_dir, mask_dir=mask_dir, transform=None, target_transform=None) #dataset object

    #setting train/test splits
    train_split = 0.8 #percentage of data to train on
    num_train = int(num_samples * 0.8) #number of train samples 
    num_test = num_samples - num_train #number of test samples

    #splitting data
    generator = torch.Generator().manual_seed(RANDOM_SEED)
    train_test_splits = torch.utils.data.random_split(dataset, [num_train, num_test], generator=generator) #splitting data randomly 
    train_set = train_test_splits[0] 
    test_set = train_test_splits[1]



    breakpoint()
    exit()
    model = UNet(in_channels=3, out_channels=2).to(device) #initializing model
    loss = nn.CrossEntropyLoss()
    # optimizer = optim.Adam(model.parameters(), lr=learning_rate)
    
    breakpoint()
    for i, (image, mask) in enumerate(dataset):
        print(i, image.shape, mask.shape)
        breakpoint()
        if i == 3: break

    trainer = Train(model=model, loss=loss, dataset=dataset)
    # print(trainer)

if __name__ == "__main__": 
    main()