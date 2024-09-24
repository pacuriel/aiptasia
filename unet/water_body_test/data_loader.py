from torch.utils.data import DataLoader

class WaterBodyDataLoader():
    def __init__(self, dataset):
        self.dataset = dataset

        data_loader = DataLoader(dataset=dataset)

        