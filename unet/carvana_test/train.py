import torch
import torch.nn
from tqdm import tqdm
from datetime import datetime
import os
import time
import numpy as np
from torchvision.utils import save_image

from utils import savePredictedMasks, plotLosses

#set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#TODO: don't hardcode hyperparams
#setting hyperparameters as global variables
# in_channels = 3 #three channels for RGB images
# num_class = 2
# learning_rate = 0.001
# num_epochs = 3 #number of epochs (full passes over training data) to train for 

#class to train U-Net
class Train:
    def __init__(self, model, loss, optimizer, train_loader, test_loader, num_epochs, train_img_dir, train_mask_dir, test_img_dir, test_mask_dir):
        """
        Input: 
        - model: class inheriting from nn.Module
        - loss: loss function
        - optimizer:  
        - dataset: 
        """
        self.model = model
        self.loss_fcn = loss
        self.optimizer = optimizer
        self.train_loader = train_loader
        self.test_loader = test_loader
        self.num_epochs = num_epochs
        self.train_img_dir = train_img_dir
        self.train_mask_dir = train_mask_dir
        self.test_img_dir = test_img_dir
        self.test_mask_dir = test_mask_dir

        #list with image/mask file names
        self.train_files = sorted(os.listdir(self.train_img_dir))
        self.test_files = sorted(os.listdir(self.test_img_dir))

        self.exp_id = datetime.now().strftime("%d-%b-%Y_%H%M_%S") #setting experiment id to current date/time
        self.exp_dir = os.path.join("experiments", self.exp_id)
        os.makedirs(name=os.path.join("experiments", self.exp_id), exist_ok=True) #creating directory to store experimental run data

        # self.save_model_path = "experiments/best_models" #directory to save best models (in terms of min. loss)

    #function to train U-Net
    def train(self):
        print("*** Starting training!")
        self.model.train() #setting model to train mode
        data_loader = self.train_loader #train dataloader
        num_batches = len(data_loader) #number of batches in train loader

        #used to determine which model to save
        best_train_loss = 1e3 
        best_test_loss = 1e3 
        train_losses = []; test_losses = [] #lists to store train/test losses per epoch
        start_time = time.time()

        #looping for preset number of epochs
        for epoch in range(self.num_epochs):
            print(f"*** Current epoch: {epoch + 1} / {self.num_epochs}") #sanity check

            loop = tqdm(data_loader) #loop object for progress bar
            epoch_loss = 0 #initializing current epoch loss to zero
            test_loss = 0

            #looping over each batch of data
            for batch_idx, (img_batch, gt_mask_batch, indices) in enumerate(loop):
                img_batch = img_batch.to(device) #batch of images
                gt_mask_batch = gt_mask_batch.float().to(device) #batch of masks (unsqueeze to add single channel dimension)
                pred_masks = self.model(img_batch) #forward pass
                loss = self.loss_fcn(pred_masks, gt_mask_batch) #calculating loss

                epoch_loss += loss.item() #updating epoch loss

                #backward pass (backprop)
                self.optimizer.zero_grad() #initializing gradients to zero
                loss.backward() #updating weights depending on gradients computed above
                self.optimizer.step() #single gradient descent step (or ADAM step)

                loop.set_postfix(loss=(epoch_loss / num_batches)) #updating tqdm bar to show loss 

            epoch_loss /= num_batches #averaging loss by number of batches
            train_losses.append(epoch_loss) #storing loss

            #saving model if current loss is best
            if epoch_loss < best_train_loss: 
                best_train_loss = epoch_loss #updating best loss
                torch.save(self.model, os.path.join(self.exp_dir, 'best_train_model.pt')) #saving model

            #applying model to test set
            test_loss = self.test(calculate_metrics=False, save_mask_arrays=True)
            test_losses.append(test_loss)
            
            #updating best test loss
            if test_loss < best_test_loss: 
                best_test_loss = test_loss
                torch.save(self.model, os.path.join(self.exp_dir, 'best_test_model.pt')) #saving model

            print(f"Epoch: {epoch + 1} / {self.num_epochs} \t Train loss: {epoch_loss} \t Best train Loss: {best_train_loss} \t Test loss: {test_loss} \t Best test Loss: {best_test_loss}\n")

        test_loss = self.test(calculate_metrics=False, save_mask_arrays=True) #running through test data to save final mask arrays

        plotLosses(train_losses, test_losses, self.num_epochs, save_dir=self.exp_dir)

        end_time = time.time()
        print(f"Total train time: {(end_time - start_time) / 60} minutes")

    #function to test U-Net on train data
    def test(self, calculate_metrics: bool = False, save_mask_imgs: bool = False, save_mask_arrays: bool = False):
        self.model.eval() #setting model to evaluate mode
        data_loader = self.test_loader #test dataloader
        num_batches = len(data_loader) #number of batches in test set
        test_loss = 0

        #telling pytorch not to calculate gradients
        with torch.no_grad():
            #looping over each batch of data
            for batch_idx, (img_batch, gt_mask_batch, indices) in enumerate(data_loader):
                img_batch = img_batch.to(device) #batch of images
                gt_mask_batch = gt_mask_batch.float().to(device) #batch of masks (unsqueeze to add single channel dimension)
                pred_masks = self.model(img_batch) #forward pass
            
                loss = self.loss_fcn(pred_masks, gt_mask_batch) #calculating loss
                test_loss += loss.item()

                pred_masks = torch.sigmoid(pred_masks) #applying sigmoid function
                pred_masks = (pred_masks >= 0.5).float() #converting to binary values

                #flag to save masks as png files
                if save_mask_imgs:
                    directory = os.path.join(self.exp_dir, "mask_images")
                    os.makedirs(name=directory, exist_ok=True)

                #flag to save masks as npy files
                if save_mask_arrays:
                    directory = os.path.join(self.exp_dir, "mask_arrays") #directory to store mask arrays
                    os.makedirs(name=directory, exist_ok=True) #creating above directory

                    #converting masks to numpy arrays
                    pred_masks = pred_masks.squeeze().cpu().numpy() 
                    
                    #looping over each predicted mask in current batch and saving
                    for i, mask in enumerate(pred_masks):
                        np.save(file=os.path.join(directory, self.test_files[indices[i]][:-3] + 'npy'), arr=mask)
                    
            test_loss /= num_batches #averaging loss by number of batches

        #TODO: use caluculate_metrics flag to call function to calculate metrics 
            #Note: above will likely have to be done per minibatch and averaged? 
        if calculate_metrics:
            pass

        self.model.train() #setting model back to train mode
        return test_loss