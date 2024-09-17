import torch
import torch.nn as nn

#class to perform double convolution 
#Note: should this be its own class???
class DoubleConv(nn.Module):
    def __init__(self, in_channels, out_channels):
        super(DoubleConv, self).__init__()

        #nn.Sequential object to perform double convolution
        self.convolve = nn.Sequential(
            nn.Conv2d(in_channels=in_channels, out_channels=out_channels, kernel_size=3, stride=1),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=out_channels, out_channels=out_channels, kernel_size=3, stride=1),
            nn.ReLU(inplace=True)
        )

    def forward(self, x):
        return self.convolve(x) #returning double convolution

#OG U-Net class that inherits from nn.Module
class UNet(nn.Module):
    #class constructor
    def __init__(self, in_channels=3, out_channels=2, feature_sizes=[64, 128, 256, 512]):
        #note: kernel_size = filter_size
        super(UNet, self).__init__()
        
        #setting member variables
        self.contract = nn.ModuleList() #stores contracting network layers (downsampling)
        self.expand = nn.ModuleList() #stores expanding network layers (upsampling)
        self.pool = nn.MaxPool2d(kernel_size=2, stride=2) #pooling layer used by U-Net 
        self.in_channels = in_channels
        self.out_channels = out_channels
        self.feature_sizes = feature_sizes

        #setting double convs for contracting path
        for feature_size in feature_sizes:
            self.contract.append(DoubleConv(in_channels=in_channels, out_channels=feature_size))

        #setting transposed convs (to upsample) and double convs for expanding path 
        for feature_size in reversed(feature_sizes):
            self.expand.append(
                nn.ConvTranspose2d(in_channels=2*feature_size, out_channels=feature_size, kernel_size=2, stride=2)
            )#append
            self.expand.append(DoubleConv(in_channels=2*feature_size, out_channels=feature_size))

    #function to perform forward pass of UNet (Note: forward fcn. is inherited from nn.Module) 
    def forward(self, x): 
        skip_connections = [] #list to store skip connections

        #contracting path (downsample)
        i = 0#counter for sanity check
        for downsample in self.contract:
            x = downsample(x) #applying double conv and ReLU
            skip_connections.append(x) #storing output for skip connections
            x = self.pool(x) #applying max pooling
            i += 1
            if i == 1:
                break #sanity check

        #expansive path (upsample)
        

        return x

if __name__ == "__main__":
    #do stuff
    img_size = 572
    num_samples = 10
    num_channels = 3
    x = torch.randn((num_samples, num_channels, img_size, img_size)) #dummy variable to represent RGB images
    print(x.shape)

    model = UNet(in_channels=3, out_channels=2) #initializing a UNet object
    preds = model(x)
    print(preds.shape)
