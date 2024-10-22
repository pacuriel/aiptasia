import torch
import torch.nn
from tqdm import tqdm

#set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#TODO: don't hardcode hyperparams
#setting hyperparameters as global variables
# in_channels = 3 #three channels for RGB images
# num_class = 2
# learning_rate = 0.001
# num_epochs = 3 #number of epochs (full passes over training data) to train for 

#class to test U-Net
class Test:
    def __init__(self, model, loss, test_loader, num_epochs: int):
        """
        Input: 
        - model: class inheriting from nn.Module
        - loss: loss function
        - optimizer:  
        - dataset: 
        """
        self.model = model
        self.loss_fcn = loss
        self.test_loader = test_loader
        # self.dataset = dataset
        self.num_epochs = num_epochs

    #function to train U-Net
    def test(self):
        print("*** Starting testing!")
        
        best_loss = 1e3 #used to determine which model to save

        #looping for preset number of epochs
        for epoch in range(self.num_epochs):
            print(f"*** Current epoch: {epoch + 1} / {self.num_epochs}") #sanity check
            num_batches = self.data_loader()
            epoch_loss = 0
            loop = tqdm(self.data_loader)
            #looping over batches of data
            for batch_idx, (img_batch, gt_mask_batch) in enumerate(loop):
            # for (img_batch, gt_mask_batch) in tqdm(self.data_loader):
                img_batch = img_batch.to(device) #batch of images
                gt_mask_batch = gt_mask_batch.float().unsqueeze(1).to(device) #batch of masks (unsqueeze to add single channel dimension)
    
                pred_masks = self.model(img_batch) #forward pass
                loss = self.loss_fcn(pred_masks, gt_mask_batch) #calculating loss

                epoch_loss += loss.item() 

                #backward pass (backprop)
                self.optimizer.zero_grad() #initializing gradients to zero
                loss.backward() #update weights depending on gradients computer above
                self.optimizer.step() #gradient descent (or ADAM step)

                loop.set_postfix(loss=(epoch_loss / len(self.data_loader))) #updating tqdm bar to show loss 

            epoch_loss /= len(self.data_loader) #averaging loss by batch size

            if epoch_loss < best_loss: #if current loss is less than best loss
                best_loss = epoch_loss #updating best loss
                #TODO: save current model checkpoint with experiment/run ID in filename

            print(f"Epoch: {epoch + 1} / {self.num_epochs} \t Loss: {epoch_loss} \t Best Loss: {best_loss}\n")