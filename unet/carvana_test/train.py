import torch
import torch.nn
from tqdm import tqdm

#set device
device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')

#TODO: don't hardcode hyperparams
#setting hyperparameters as global variables
in_channels = 3 #three channels for RGB images
num_class = 2
learning_rate = 0.001
batch_size = 1 #size of each batch to train on
num_epochs = 10 #number of epochs (full passes over training data) to train for 

#class to train U-Net
class Train:
    def __init__(self, model, loss, optimizer, scheduler):
        """
        Input: 
        - model: class inheriting from nn.Module
        - loss: loss function
        - optimizer:  
        - dataset: 
        """
        self.model = model
        self.loss = loss
        self.optimizer = optimizer
        # self.dataset = dataset

    #function to train U-Net
    def train(self):
        #for loop to train
        for epoch in (tqdm(range(num_epochs))):
            #loop over each batch of data
            for batch_idx, (data, targets) in enumerate(self.dataset):
                if batch_idx % 50 == 0:
                    print(f"Training on batch {batch_idx}") #sanity check
            
                #move data/targets to device
                data = data.to(device=device)
                targets = targets.to(device=device)

                scores = self.model(data) #forward pass
                loss = self.loss(scores, targets) #calculating loss on one batch of data

                #backward pass (backprop)
                self.optimizer.zero_grad() #set gradients to zero initially
                loss.backward() #update weights depending on gradients computed above

                #gradient descent (or ADAM step)
                self.optimizer.step()
        