import torch
import torch.nn

#class to train U-Net
class Train:
    def __init__(self, model, loss, dataset):
        """
        Input: 
        - model: class inheriting from nn.Module
        - loss: loss function 
        - 
        """
        self.model = model
        self.loss = loss

    #function to train U-Net
    def train(self):
        pass