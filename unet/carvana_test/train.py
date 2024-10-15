import torch
import torch.nn
from tqdm import tqdm
from datetime import datetime
import os
import time

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
    def __init__(self, model, loss, optimizer, train_loader, test_loader, num_epochs: int):
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
        
        self.exp_id = datetime.now().strftime("%d-%b-%Y_%H%M_%S") #setting experiment id to current date/time
        self.save_model_path = "experiments/best_models" #directory to save best models (in terms of min. loss)

    #function to train U-Net
    def train(self):
        print("*** Starting training!")
        
        best_loss = 1e3 #used to determine which model to save
        
        start_time = time.time()

        #looping for preset number of epochs
        for epoch in range(self.num_epochs):
            print(f"*** Current epoch: {epoch + 1} / {self.num_epochs}") #sanity check

            num_batches = len(self.train_loader) #number of batches in train loader
            loop = tqdm(self.train_loader) #loop object for progress bar
            epoch_loss = 0 #initializing current epoch loss to zero

            #looping over each batch of data
            for batch_idx, (img_batch, gt_mask_batch) in enumerate(loop):
            # for (img_batch, gt_mask_batch) in tqdm(self.data_loader):
                img_batch = img_batch.to(device) #batch of images
                gt_mask_batch = gt_mask_batch.float().unsqueeze(1).to(device) #batch of masks (unsqueeze to add single channel dimension)
    
                pred_masks = self.model(img_batch) #forward pass
                loss = self.loss_fcn(pred_masks, gt_mask_batch) #calculating loss

                epoch_loss += loss.item() 

                #backward pass (backprop)
                self.optimizer.zero_grad() #initializing gradients to zero
                loss.backward() #updating weights depending on gradients computed above
                self.optimizer.step() #single gradient descent step (or ADAM step)

                loop.set_postfix(loss=(epoch_loss / len(self.train_loader))) #updating tqdm bar to show loss 

            epoch_loss /= num_batches #averaging loss by batch size

            if epoch_loss < best_loss: #if current loss is less than best loss
                best_loss = epoch_loss #updating best loss
                #TODO: save current model checkpoint with experiment/run ID in filename
                torch.save(self.model, os.path.join(self.save_model_path, self.exp_id + '.pt'))

            print(f"Epoch: {epoch + 1} / {self.num_epochs} \t Loss: {epoch_loss} \t Best Loss: {best_loss}\n")

        end_time = time.time()
        print(f"Total train time: {(end_time - start_time)} seconds")