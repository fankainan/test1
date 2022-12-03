#!/usr/bin/python
# -*- coding: utf-8 -*-
# @Time   : 2021/1/27 10:50
# @Author : SandQuant

import collections
from win32 import win32gui
import pyautogui
import sys
import time
from mytools import colorPrint


class PySpy(object):
    Window = collections.namedtuple(
        'Window', ['caption', 'class_name', 'hwnd_py', 'hwnd_spy'])

    def __init__(self):
        pass

    @classmethod
    def window_attr(cls, hwnd_py):  # 窗口属性
        """
        显示窗口的属性
        :param hwnd_py: 窗口句柄（十进制）
        :return: Window
        """
        return cls.Window(
            caption=win32gui.GetWindowText(hwnd_py),
            class_name=win32gui.GetClassName(hwnd_py),
            hwnd_py=hwnd_py,
            hwnd_spy=hex(hwnd_py),
        )

    @classmethod
    def show_top_windows(cls):
        """
        列出所有的顶级窗口及属性
        :return: 全部的顶层窗口及对应属性
        """
        containers = []
        win32gui.EnumWindows(lambda hwnd, param: param.append(
            cls.window_attr(hwnd)), containers)
        return containers

    @classmethod
    def find_top_window(cls, caption) -> list:
        """
        查找窗体
        :param caption: 窗口标题部分文字
        :return:
        """
        return [w for w in cls.show_top_windows() if caption in w.caption]

    @classmethod
    def find_sub_windows(cls, hwnd_py=None, class_name=None, caption=None, index=None):
        """
        返回窗体下全部的子窗体，默认主窗体下的窗体
        :param hwnd_py: 句柄 十进制
        :param class_name: 窗口类名，返回特定类名
        :param caption: 窗口标题，返回特定标题
        :param index: 位置，返回特定位置的窗口
        :return: 包含属性的全部子窗口
        """
        num = 0
        handle = 0
        sub_windows = []
        while True:
            # find next handle, return HwndPy
            handle = win32gui.FindWindowEx(
                hwnd_py, handle, class_name, caption)
            if handle == 0:
                # no more handle
                break
            # get handle attribution
            attr = cls.window_attr(handle)
            # append to list
            sub_windows.append(tuple(list(attr) + [num]))
            num += 1
        if index is not None:
            return sub_windows[index]
        else:
            return sub_windows

    @classmethod
    def show_all_windows(cls, window=None, handle_list=None, handle_dict=None):
        """
        生成窗口全部对应的关系
        :param window: 目标父窗口
        :param handle_list: 默认为[[None]]
        :param handle_dict: 用于存放对应关系
        :return: 返回目标窗口下全部子父窗口的字典
        """
        if not handle_list and not handle_dict:
            handle_list = [[None]]
            handle_dict = dict()
        sys.setrecursionlimit(1000000)
        if window:
            handle_list[-1][0] = window
            handles = cls.find_sub_windows(handle_list[-1][0][2])
        else:
            handles = cls.find_sub_windows()
        for handle in handles:
            handle_dict[handle] = window
        # 这个根节点已经遍历完，删除
        del handle_list[-1][0]
        # 如果有叶节点，非空，则加入新的叶节点
        if handles:
            handle_list.append(handles)
        # 删除已被清空的根
        handle_list = [
            HandleGroup for HandleGroup in handle_list if HandleGroup]
        # 如果还有根就继续遍历，否则输出树
        if handle_list:
            return cls.show_all_windows(window=handle_list[-1][0], handle_list=handle_list, handle_dict=handle_dict)
        else:
            return handle_dict

    @classmethod
    def find_handle_path(cls, hwnd_spy, num):
        """
        寻找特定窗口的寻找路径
        找到全部层级的对应关系，然后反向搜索
        :param hwnd_spy: 窗口句柄（十六进制）
        :param num: 窗口所属index，在spy++内查看
        :return:
        parent_window：顶层窗口
        target_path：路径的index
        """
        all_path = cls.show_all_windows()
        key = tuple(list(cls.window_attr(int(hwnd_spy))) + [num])
        handle_path = [key]
        while True:
            key = all_path[key]
            if not key:
                handle_path = handle_path[::-1]
                parent_window = handle_path[0]
                target_path = [(i[-1]) for i in handle_path[1:]]
                return parent_window, target_path
            handle_path.append(key)

    @classmethod
    def find_target_handle(cls, window, path):
        """
        递归寻找子窗口的句柄
        :param window: 祖父窗口的完整句柄 (WindowName, ClassName, HwndPy, HwndSpy)
        :param path: 子窗口列表
        :return: 目标窗口的完整属性
        """
        for i in range(len(path)):
            window = cls.find_sub_windows(window[2], index=path[i])
        return window

    @classmethod
    def FindFuzzyTopWindows(cls, FuzzyWindowName=None) -> list:
        """根据标题模糊查找全部符合条件的主窗体

        Args:
            FuzzyWindowName (_type_, optional): 窗口标题部分文字. Defaults to None.

        Returns:
            list: 列表，里面元素是元组
        """

        all_windows = cls.show_top_windows()
        result = []
        for window in all_windows:
            if FuzzyWindowName in window[0]:
                result.append(window)
        return result


# 以下来自https://www.mianshigee.com/note/detail/10302upx/教程

if __name__ == '__main__':

    # 列出所有窗口
    colorPrint.red('列出所有窗口'.ljust(50, '*'))
    result = PySpy.show_top_windows()
    for item in result:
        print(item, type(item))
        

    findone = PySpy.FindFuzzyTopWindows('记事本')
    print(findone, type(findone))
    colorPrint.blue(findone[0])

    another = PySpy.find_sub_windows(getattr(findone[0], 'hwnd_py'))
    print(another)

    handle = win32gui.FindWindowEx(
        getattr(findone[0], 'hwnd_py'), None, None, None)
    print(handle)
    hwnd = 133444 #句柄应该是其他方法获取到的
    win32gui.SetForegroundWindow(hwnd)