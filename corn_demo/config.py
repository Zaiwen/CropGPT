import argparse
import os
from functools import partial
from utils import get_path
from datetime import datetime


def get_parser(name):
    """
    函数使用functools模块的partial函数修改了parser对象的add_argument方法，
    以添加一个默认help参数，其值为一个空字符串。这意味着每当使用add_argument方法向parser对象添加新参数时，
    它将自动具有一个默认的帮助消息，其描述为一个空字符串.
    """
    parser = argparse.ArgumentParser(name, formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument = partial(parser.add_argument, help=' ')
    return parser


class BaseConfig(argparse.Namespace):
    def print_params(self, prtf=print):
        """
        它按字母顺序打印出self对象的所有属性的值。使用vars()函数获取self对象的所有属性和它们的值的字典，
        然后使用sorted()函数按键进行排序。
        该方法使用format()方法和属性名称的upper()方法将输出格式化为字符串。
        """
        prtf("")
        prtf("Parameters:")
        for attr, value in sorted(vars(self).items()):
            prtf("{}={}".format(attr.upper(), value))
        prtf("")

    def as_markdown(self):
        """
        该方法返回一个以Markdown格式包含self对象的所有属性和它们的值的表格的字符串。
        它使用与print_params()方法类似的方法将输出格式化为字符串。
        """
        text = "|name|value|  \n|-|-|  \n"
        for attr, value in sorted(vars(self).items()):
            text += "|{}|{}|  \n".format(attr, value)
        return text


class Config(BaseConfig):
    def build_parser(self):
        parser = get_parser("config")
        parser.add_argument('--name', type=str, default="DTT", help="DTT/PH/EW")
        parser.add_argument('--diquname', type=str, default="JL", help="BJ/HN/JL/LN")
        parser.add_argument('data', type=str, default="example1.txt", help=".txt/AGCT")
        return parser

    def __init__(self):
        parser = self.build_parser()
        args = parser.parse_args()
        super().__init__(**vars(args))


if __name__ == "__main__":
    config = Config()
    config.print_params()


