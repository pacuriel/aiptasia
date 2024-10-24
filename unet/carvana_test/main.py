"""
Main file to test original U-Net model on water body dataset
Pablo A. Curiel
October 2024
"""
import platform
import os
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import DataLoader

# from unet_OG import UNet #importing OG U-Net Model
from unet_padded import UNet
from data import ImageDataset #dataset class
from train import Train

RANDOM_SEED = 42 #random seed for testing (not so random i guess?)
torch.manual_seed(RANDOM_SEED)

#setting hyperparameters as global variables
#TODO: don't hardcode hyperparams
in_channels = 3 #three channels for RGB images
out_channels = 1
learning_rate = 1e-3 #learning rate used by optimizer
batch_size = 16 #size of each batch to train on
num_epochs = 20 #number of epochs (full passes over training data) to train for 
#setting global variables
device = "cuda" if torch.cuda.is_available() else "cpu" #device for pytorch

TILE_SIZE = 512

###Note: sample initial weigths from a Gaussian distribution w/ std_dev = sqrt(2 / N), where N = # incoming nodes (per last paragraph of section 3) 

#function to store directories w/ data
def storeDirs(input_size: int = None, output_size: int = None) -> tuple[str, str]:
    #storing image and mask directories
    if platform.system() == "Linux":
        root_dir = "/home/pcuriel/data/aiptasia/image_data/carvana_data/"
        train_img_dir = root_dir + "train_images/" + f"tiles_{TILE_SIZE}"
        train_mask_dir = root_dir + "train_masks/" + f"tiles_{TILE_SIZE}"
        test_img_dir = root_dir + "test_images/" + f"tiles_{TILE_SIZE}"
        test_mask_dir = root_dir + "test_masks/" + f"tiles_{TILE_SIZE}"
    elif platform.system() == "Windows": 
        image_dir = "C:\\Users\\giant\\Desktop\\aiptasia\\data\\carvana_data\\subset_tiles"
        mask_dir = "C:\\Users\\giant\\Desktop\\aiptasia\\data\\carvana_data\\subset_masks_tiles"

    return train_img_dir, train_mask_dir, test_img_dir, test_mask_dir

def main(): 
    train_mode = True #tells model whether to update parameters

    train_img_dir, train_mask_dir, test_img_dir, test_mask_dir = storeDirs() #calling function to store paths to img/mask data

    train_set = ImageDataset(image_dir=train_img_dir, mask_dir=train_mask_dir)
    train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)

    test_set = ImageDataset(image_dir=test_img_dir, mask_dir=test_mask_dir)
    test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=False)

    # num_samples = len(os.listdir(image_dir)) #total number of data samples available
    
    # #TODO: determine what transforms to apply
    # dataset = ImageDataset(image_dir=image_dir, mask_dir=mask_dir, transform=None, target_transform=None) #dataset object representing all img/mask data
    # #setting train/test splits
    # train_split = 0.8 #percentage of data to train on
    # num_train = int(num_samples * train_split) #number of train samples 
    # num_test = num_samples - num_train #number of test samples

    # #splitting data
    # generator = torch.Generator().manual_seed(RANDOM_SEED)
    # train_test_splits = torch.utils.data.random_split(dataset, [num_train, num_test], generator=generator) #splitting data randomly 
    # train_set = train_test_splits[0] 
    # test_set = train_test_splits[1]

    # #preparing data for training with dataloaders
    # train_loader = DataLoader(train_set, batch_size=batch_size, shuffle=True)
    # test_loader = DataLoader(test_set, batch_size=batch_size, shuffle=True)
    
    model = UNet(in_channels=in_channels, out_channels=out_channels).to(device) #U-Net model

    if train_mode: model.train() #setting model to train mode

    loss_fcn = nn.BCEWithLogitsLoss() #loss function (combination of Sigmoid layer and BCELoss; similar to original paper) 
    optimizer = optim.Adam(model.parameters(), lr=learning_rate) #parameter optimizer

    #calling train class to begin training model
    trainer = Train(model=model,
                    loss=loss_fcn, 
                    optimizer=optimizer, 
                    train_loader=train_loader,
                    test_loader=test_loader,
                    num_epochs=num_epochs,
                    train_img_dir=train_img_dir,
                    train_mask_dir=train_mask_dir,
                    test_img_dir=test_img_dir,
                    test_mask_dir=test_mask_dir)

    trainer.train() #calling function to train model

    #TODO: evaluate model on test set
    # train_mode = False #updating train mode
    # model.eval() #setting model to evaluate mode

if __name__ == "__main__": 
    main()
