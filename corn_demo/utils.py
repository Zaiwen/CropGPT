import logging
import numpy as np
from torch.utils.data import Dataset
import torch
import os.path
from torch import nn
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
import shutil
import pathlib


def bulit_logger(file_path):
    """制作一个Python日志，便于保存实验记录"""
    my_logger = logging.getLogger('my_logger')
    log_format = '%(asctime)s | %(message)s'
    formatter = logging.Formatter(log_format, datefmt='%m/%d %I:%M:%S %p')
    file_handler = logging.FileHandler(file_path)
    file_handler.setFormatter(formatter)
    stream_handler = logging.StreamHandler()
    stream_handler.setFormatter(formatter)
    my_logger.addHandler(file_handler)
    my_logger.addHandler(stream_handler)
    my_logger.setLevel(logging.INFO)
    return my_logger


def standardization_mu_sigama(da):
    """计算并输出训练集的均值和标准差"""
    mu = np.mean(da, axis=0)
    sigma = np.std(da, axis=0)
    return mu, sigma


def standardization(da, mu, sigma):
    """
    根据均值和标准差得到标准化数据
    :param da: 数据
    :param mu: 均值
    :param sigma: 标准差
    :return: 标准化后的数据
    """
    return (da - mu) / sigma


class Mydataset_xy(Dataset):
    """设置生成器，批次预处理再进入模型"""
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, item):
        x = self.x[item]
        y = self.y[item]
        y = np.array(y)
        x = torch.from_numpy(x).type(torch.float)
        y = y.astype(np.float32)
        y = torch.from_numpy(y).type(torch.float)
        return x, y

    def __len__(self):
        return len(self.x)


class Mydataset_xyz(Dataset):
    """设置生成器，批次预处理再进入模型"""
    def __init__(self, x, y, z, train=False):
        self.x = x
        self.y = y
        self.z = z
        self.train = train

    def __getitem__(self, item):
        x = self.x[item]
        y = self.y[item]
        z = self.z[item]
        y = np.array(y)
        x = np.expand_dims(np.array(x), axis=0)
        # x = np.expand_dims(np.array(x), axis=0)
        x = torch.from_numpy(x).type(torch.float)
        if self.train:
            x = x + (20*torch.rand(3, 64, 64) - 10)
        y = y.astype(np.float32)
        y = torch.from_numpy(y).type(torch.float)
        z = np.array(z).reshape(1, -1)
        z = torch.from_numpy(z).type(torch.LongTensor)
        return x, y, z

    def __len__(self):
        return len(self.x)


def save_model(state, p_name, is_best=False):
    """保存较优模型"""
    if is_best:
        best_filename = os.path.join(f'{p_name}/best_model.pth.tar')
        torch.save(state, best_filename)


def init_weights(m):
    """针对不同类型的层使用不同的初始化方法"""
    # 如果是卷积层
    if type(m) == nn.Conv2d:
        # torch.nn.init.normal_(m.weight, mean=0, std=0.5)
        # torch.nn.init.kaiming_normal_(m.weight, mode="fan_in", nonlinearity="relu")
        torch.nn.init.xavier_uniform_(m.weight.data)
        # torch.nn.init.constant_(m.bias, 0.1)
    # 如果是全连接层
    if type(m) == nn.Linear:
        m.weight.data.normal_(0, 0.01)
        # m.bias.data.zero_()
    if type(m) == nn.BatchNorm2d:
        # m.weight.data.fill_(1)
        m.bias.data.zero_()
    # torch.nn.init.kaiming_normal(m.weight, mode="fan_in", nonlinearity="relu")



def my_qqplot(y_t, y_p, path, name):
    """
    绘制QQ图
    :param y_t: 测试集真值
    :param y_p: 测试集预测值
    :param project_name: 项目名称 以便保存图片
    :return:
    """
    y_pp = pd.DataFrame()
    y_pp["y_t"] = np.percentile(y_t, range(100))
    y_pp["y_p"] = np.percentile(y_p, range(100))
    plt.figure(figsize=(8, 8))
    # plt.scatter(x='y_t', y='y_p', data=y_pp, label='Actual fit')
    plt.scatter(y_t, y_p, label='Actual fit')
    sns.lineplot(x='y_t', y='y_t', data=y_pp, color='r', label='Line of perfect fit')
    plt.xlabel("test", fontsize=20)
    plt.ylabel("pre", fontsize=20)
    plt.tick_params(labelsize=15)
    plt.legend(fontsize=20)
    plt.title("QQ_plot", fontsize=20)
    plt.savefig(f'{path}/{name}.jpg')
    # plt.show()
    plt.clf()


def my_qqplot_bf(y_t, y_p, path, name):
    """
    绘制QQ图
    :param y_t: 测试集真值
    :param y_p: 测试集预测值
    :param project_name: 项目名称 以便保存图片
    :return:
    """
    y_pp = pd.DataFrame()
    y_pp["y_t"] = np.percentile(y_t, range(100))
    y_pp["y_p"] = np.percentile(y_p, range(100))
    plt.figure(figsize=(8, 8))
    plt.scatter(x='y_t', y='y_p', data=y_pp, label='Actual fit')
    # plt.scatter(y_t, y_p, label='Actual fit')
    sns.lineplot(x='y_t', y='y_t', data=y_pp, color='r', label='Line of perfect fit')
    plt.xlabel("test", fontsize=20)
    plt.ylabel("pre", fontsize=20)
    plt.tick_params(labelsize=15)
    plt.legend(fontsize=20)
    plt.title("QQ_plot", fontsize=20)
    plt.savefig(f'{path}/{name}_bf.jpg')
    # plt.show()
    plt.clf()


def my_qqplot_yanse(y_t, y_p, path, name):
    """
    绘制QQ图
    :param y_t: 测试集真值
    :param y_p: 测试集预测值
    :param project_name: 项目名称 以便保存图片
    :return:
    """
    y_pp = pd.DataFrame()
    y_pp["y_t"] = np.percentile(y_t, range(100))
    plt.figure(figsize=(8, 8))
    y_pp1 = pd.DataFrame()
    y_pp1["X"] = pd.DataFrame(np.array(y_t).reshape(-1, 1))
    y_pp1["Y"] = pd.DataFrame(np.array(y_p).reshape(-1, 1))
    # 统计每个坐标点的数据个数
    # 绘制散点图
    sns.set_style('whitegrid')
    ax = sns.scatterplot(data=y_pp1, x='X', y='Y', alpha=0.5)

    # 绘制密度图
    sns.kdeplot(data=y_pp1, x='X', y='Y', cmap='Reds', thresh=0.05, fill=True, alpha=0.5, ax=ax)
    sns.lineplot(x='y_t', y='y_t', data=y_pp, color='r', label='Line of perfect fit')
    plt.xlabel("test", fontsize=20)
    plt.ylabel("pre", fontsize=20)
    plt.tick_params(labelsize=15)
    # plt.legend(fontsize=20)
    plt.title("QQ_plot", fontsize=20)
    plt.savefig(f'{path}/{name}_yanse.jpg')
    # plt.show()
    plt.clf()

def get_path(my_path):
    """
    判断是否存在该路径而已
    """
    if not os.path.exists(my_path):
        os.makedirs(my_path)
    return my_path


def log_csv(best_epoch, train, valid, test, config):
    """
    用来自动记录不同训练结果，而不用每次自动手动选择
    :param sota: 预测的具体表型
    :param comfig: 配置参数
    """
    csv_path = os.path.join(config.got_csv, "all.csv")
    if not os.path.exists(csv_path):
        csv_log = pd.DataFrame()
        a1 = []
        a2 = []
        for attr, value in sorted(vars(config).items()):
            a1 += [str(attr)]
            a2 += [str(value)]
        a1 = ["project_name", "sota", "diqu", "seed", "best_epoch", "train_r2", "valid_r2", "all_test_r2", "test_r2", "test_r"] + a1
        if len(config.mydiqu) == 1:
            a2 = [config.project_name, config.name, config.mydiqu, config.seed,
                  best_epoch, train, valid, test, config.testlog, np.sqrt(config.testlog)] + a2
        else:
            a2 = [config.project_name, config.name, ",".join(config.mydiqu), config.model, config.dataset_x, config.seed,
                  best_epoch, train, valid, test, ",".join(str(i) for i in config.testlog), ",".join(str(np.sqrt(i)) for i in config.testlog)] + a2
        for j, i in enumerate(a2):
            csv_log.loc[0, j] = i
        csv_log.columns = a1
        csv_log.to_csv(csv_path, index=False)
    else:
        csv_log = pd.read_csv(csv_path, dtype=object)
        csv_log = pd.DataFrame(csv_log)
        b = len(csv_log)
        a1 = []
        a2 = []
        for attr, value in sorted(vars(config).items()):
            a1 += [str(attr)]
            a2 += [str(value)]
        a1 = ["project_name", "sota", "diqu", "seed", "best_epoch", "train_r2", "valid_r2", "all_test_r2", "test_r2", "test_r"] + a1
        if len(config.mydiqu) == 1:
            a2 = [config.project_name, config.name, config.mydiqu, config.seed,
                  best_epoch, train, valid, test, config.testlog, np.sqrt(config.testlog)] + a2
        else:
            a2 = [config.project_name, config.name, ",".join(config.mydiqu), config.model, config.dataset_x, config.seed,
                  best_epoch, train, valid, test, ",".join(str(i) for i in config.testlog), ",".join(str(np.sqrt(i)) for i in config.testlog)] + a2
        csv_log.loc[b, :] = a2
        csv_log.columns = a1
        csv_log.to_csv(csv_path, index=False)


def diqu_png(data1, data2, config, num):
    if num == 0 :
        y_t, y_p = np.squeeze(np.array(data1)[:int(config.y_test[0, 0])]), np.squeeze(np.array(data2)[:int(config.y_test[0, 0])])
        save_data = pd.concat([pd.DataFrame(np.expand_dims(y_t, axis=1)), pd.DataFrame(np.expand_dims(y_p, axis=1))], axis=1)
        save_data.columns = ["y_t", "y_p"]
        save_data.to_csv(f"{config.path}/test_tp_{num}.csv")
    elif num > 0:
        y_t, y_p = np.squeeze(np.array(data1)[int(config.y_test[num-1, 0]):int(config.y_test[num, 0])]), np.squeeze(np.array(data2)[int(config.y_test[num-1, 0]):int(config.y_test[num, 0])])
        save_data = pd.concat([pd.DataFrame(np.expand_dims(y_t, axis=1)), pd.DataFrame(np.expand_dims(y_p, axis=1))], axis=1)
        save_data.columns = ["y_t", "y_p"]
        save_data.to_csv(f"{config.path}/test_tp_{num}.csv")
