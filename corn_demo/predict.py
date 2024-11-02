from coding import coding
from config import Config
import numpy as np
import torch

config = Config()
device = torch.device('cpu')
model_path = f"/home/zwfeng4/CropGPT-main/corn_demo/model/{config.name}_{config.diquname}_best_model.pth.tar"
net = torch.load(model_path, map_location=torch.device('cpu'))
if "." in config.data:
    data_x = open(f'{config.data}').read()
else:
    data_x = config.data
data_x = np.expand_dims(coding(data_x), axis=0)

net.eval()
with torch.no_grad():
    # print(data_x.shape)
    data_y_pre = net(torch.from_numpy(data_x).type(torch.float).to(device), torch.from_numpy(np.zeros((64, 1, 1))).type(torch.float).to(device))
    print(float(data_y_pre))


# model_path = f"C:\\Users\\Roied\Desktop\\新建文件夹\\Code\\code\\project\\maize_model\\{config.name}_{config.diquname}_best_model.pth.tar"


