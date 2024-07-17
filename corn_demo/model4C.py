from torch import nn
import torch.nn.functional as F
import torch


class MyVGG4c(nn.Module):
    """自主修改的resnet模型架构"""
    def __init__(self):
        super(MyVGG4c, self).__init__()
        self.layer1 = nn.Sequential(
            nn.Conv2d(in_channels=1, out_channels=8, kernel_size=(4, 3), stride=1, padding=(0, 1)),
            nn.BatchNorm2d(8),
            nn.ReLU(inplace=True),
            nn.Conv2d(in_channels=8, out_channels=16, kernel_size=(1, 3), stride=2, padding=(0, 1)),
            nn.BatchNorm2d(16),
            nn.ReLU(inplace=True),
            # nn.Conv2d(in_channels=16, out_channels=32, kernel_size=(1, 5), stride=2, padding=(0, 2)),
            # nn.BatchNorm2d(32),
            # nn.ReLU(inplace=True),
        )
        self.layer2 = make_layer(16, 16, 2, stride=1)
        self.layer3 = make_layer(16, 32, 3, stride=2)
        self.se = SELayer(16)
        self.fc1 = nn.Sequential(
            nn.Linear(48000, 1024),
            nn.ReLU(inplace=True),
            # nn.Dropout(0.1),
            nn.Linear(1024, 256),
            nn.ReLU(inplace=True),
            nn.Linear(256, 1),
        )


    def forward(self, x, z):
        # print(x.shape)
        x = self.layer1(x)
        # print(x.shape)
        # x = self.layer3(x)
        x = self.se(x)
        # print(x.shape)
        x = x.view(len(x), -1)
        # print(x.shape)
        return self.fc1(x)


class Block(nn.Module):
    def __init__(self, in_channel, out_channel, strides=1, same_shape=True):
        super(Block, self).__init__()
        self.same_shape = same_shape
        if not same_shape:
            strides = 2
        self.strides = strides
        self.block = nn.Sequential(
            nn.Conv2d(in_channel, out_channel, kernel_size=(1, 11), stride=strides, padding=(0, 5), bias=False),
            nn.BatchNorm2d(out_channel),
            nn.ReLU(inplace=True),
            nn.Conv2d(out_channel, out_channel, kernel_size=(1, 11), padding=(0, 5), bias=False),
            nn.BatchNorm2d(out_channel),
            SELayer(out_channel)
        )
        if not same_shape:
            self.conv3 = nn.Conv2d(in_channel, out_channel, kernel_size=(1, 1), stride=strides, bias=False)
            self.bn3 = nn.BatchNorm2d(out_channel)

    def forward(self, x):
        out = self.block(x)
        if not self.same_shape:
            x = self.bn3(self.conv3(x))
        return F.relu(out + x)


def make_layer(in_channel, out_channel, block_num, stride=1):
    layers = []
    if stride != 1:
        layers.append(Block(in_channel, out_channel, stride, same_shape=False))
    else:
        layers.append(Block(in_channel, out_channel, stride))

    for i in range(1, block_num):
        layers.append(Block(out_channel, out_channel))
    return nn.Sequential(*layers)


# SE_NET
class SELayer(nn.Module):
    def __init__(self, ch_in, reduction=16):
        super(SELayer, self).__init__()
        self.avg_pool = nn.AdaptiveAvgPool2d(1)  # 全局自适应池化
        self.fc = nn.Sequential(
            nn.Linear(ch_in, ch_in // reduction, bias=False),
            nn.ReLU(inplace=True),
            nn.Linear(ch_in // reduction, ch_in, bias=False),
            nn.Sigmoid()
        )

    def forward(self, x):
        b, c, _, _ = x.size()
        y = self.avg_pool(x).view(b, c)  # squeeze操作
        y = self.fc(y).view(b, c, 1, 1)  # FC获取通道注意力权重，是具有全局信息的
        return x * y.expand_as(x)  # 注意力作用每一个通道上
