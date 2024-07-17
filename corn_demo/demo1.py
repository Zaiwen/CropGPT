import numpy as np
from coding import coding
from utils import *
from config import Config

config = Config()
device = torch.device('cuda')
net = torch.load(f'./best_model.pth.tar').to(device)
if "." in config.data:
    data_x = open(f'{config.data}').read()
else:
    data_x = config.data
data_x = np.expand_dims(coding(data_x), axis=0)
if config.diquname == "BJ":
    data_x_1 = 0
elif config.diquname == "HN":
    data_x_1 = 1
elif config.diquname == "JL":
    data_x_1 = 2
elif config.diquname == "LN":
    data_x_1 = 3

net.eval()
with torch.no_grad():
    # print(data_x.shape)
    data_y_pre = net(torch.from_numpy(data_x).type(torch.float).to(device), torch.from_numpy(np.zeros((64, 1, 1))).type(torch.float).to(device))
    print(config.name, config.diquname, float(data_y_pre))



