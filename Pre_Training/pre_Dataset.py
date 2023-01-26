import torch.utils.data as data
import torch


class pre_Dataset(data.Dataset):
    def __init__(self, data_tensor, target_tensor):
        super(pre_Dataset, self).__init__()

        self.data_tensor = torch.tensor(data_tensor)
        self.target_tensor = torch.tensor(target_tensor)

    def __len__(self):
        return len(self.data_tensor)

    def __getitem__(self, item):
        return self.data_tensor[item][:4], self.target_tensor[item]
