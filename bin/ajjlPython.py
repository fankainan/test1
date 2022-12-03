import pyautogui as pag
import time
import sys
import os
import collections
import win32gui
import win32con
import win32api
import keyboard
import time
import pyperclip

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print('获取当前工作目录路径', os.getcwd())  # 获取当前工作目录路径
print("初始化工作目录,避免在CLI中出现相对路径的运行错误问题")
dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
os.chdir(dirname)
print(f"修改工作目录为 {dirname}")


# os.chdir(os.path.dirname(__file__))
sys.path.append('../lib')
from mytools import basicClass, colorPrint  # NOQA: E402
from mytools import myNowTime, checkKeyWord  # NOQA: E402


# 版本说明：
# v1.2 2022.10.16 增加 setWindowPos,增加一些注释   2022.09.06 修复mytools相对导入的bug  2022.09.03 增加热键触发2021.04.18 新建
# 功能说明： 模拟鼠标键盘
# 备注说明：
# 环境要求： 在window10测试通过,需要安装pyautogui
# 设备要求： win10测试通过


class ajjl(basicClass):
    """
    这个是一个按键精灵的python版本,可以模拟鼠标键盘的操作
    """
    VERSION = 'v1.2 2022.10.16'
    Window = collections.namedtuple(
        'Window', ['caption', 'class_name', 'hwnd_py', 'hwnd_spy'])

    def __init__(self):
        super().__init__()
        self.instanceName = '按键精灵: '
        pag.PAUSE = 0.1
        pag.FAILSAFE = True  # 保护措施,避免失控.鼠标放到0,0的位置就可以结束脚本
        self.screenWidth, self.screenHeight = pag.size()
        VERSION = '1.0 2022.09.03'
        self.initialPosition = (0, 0)

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

    def FindFuzzyTopWindows(self, FuzzyWindowName=None) -> list:
        """根据标题模糊查找全部符合条件的主窗体
           返回值为windows对象组成的列表, 可能为空[]

        Args:
            FuzzyWindowName (_type_, optional): 窗口标题部分文字. Defaults to None.

        Returns:
            list: 列表，里面元素是window对象元组
        """
        all_windows = self.show_top_windows()
        result = []
        for window in all_windows:
            if FuzzyWindowName in window[0]:
                result.append(window)
        self.classPrint(f'查找到符合 #{FuzzyWindowName}# 的句柄 {len(result)}个')
        return result

    def alert(self, text, title):
        self.classPrint("弹出提示", text)
        pag.alert(text=text, title=title)

    def dragTo(self, srcPos, dstPos, duration=1):
        """点击后拖动对象到目的地, 采用绝对地址

        Args:
            srcPos (int): x坐标
            dstPos (int): y坐标
            duration (int, optional): _description_. Defaults to 2.
        """
        self.classPrint(f'点击后拖动对象到绝对地址')
        # 开始快速移动，接近目的地时变慢。
        pag.dragTo(x=srcPos, y=dstPos, duration=duration,
                   tween=pag.easeOutQuad)

    def dragRel(self, xOffset, yOffset, duration=1):
        """点击后拖动对象到 相对位置

        Args:
            xOffset (int): x偏移量
            yOffset (int): y偏移量
            duration (int, optional): 执行时间. Defaults to 2.
        """
        #
        self.classPrint(f'点击后拖动对象到绝对地址')
        # 开始快速移动，接近目的地时变慢。
        pag.dragRel(xOffset, yOffset, duration=duration,
                    tween=pag.easeOutQuad)

    def dumpWindow(self, hwnd, wantedText=None, wantedClass=None):
        '''
        :param hwnd: 窗口句柄,
        :param wantedText: 指定子窗口名
        :param wantedClass: 指定子窗口类名
        :return: 返回父窗口下所有子窗体的句柄
        '''
        windows = []
        hwndChild = None
        while True:
            hwndChild = win32gui.FindWindowEx(
                hwnd, hwndChild, wantedClass, wantedText)
            if hwndChild:
                textName = win32gui.GetWindowText(hwndChild)
                className = win32gui.GetClassName(hwndChild)
                windows.append((hwndChild, textName, className))
            else:
                return windows

    def getCurPosition(self) -> tuple:
        """获取当前鼠标坐标点

        Returns:
            tuple: 坐标点元组(x，y)
        """
        x, y = pag.position()
        posStr = "当前鼠标位置:" + str(x).rjust(4) + ',' + str(y).rjust(4)
        # 打印当前鼠标位置坐标
        self.classPrint(posStr)
        return x, y

    def getNowWinHwnd(self) -> int:
        """获取当前窗口句柄

        Returns:
            int: 窗口句柄,十进制的
        """
        # 获取激活窗口句柄
        hwnd = win32gui.GetForegroundWindow()
        self.classPrint(f'获取当前活动的窗口的句柄 {hwnd}')
        return hwnd

    def getChildTexts(self, parentTitle: str) -> list:
        """获取parentTitle父窗口标题下的所有子句柄的文本,
           正常是用于对话框

        Args:
            parentTitle (str): 父窗口的标题, 大小写不区分

        Returns:
            list: 包含字符的列表
        """
        # 通过窗口标题查找窗口,返回值为(hwndChild, textName, className)的列表
        # 查找模式是找第一个
        # 父窗口句柄, 参数1是类名，参数2是标题
        dialogHwnd = win32gui.FindWindow(None, parentTitle)
        if dialogHwnd:

            list1 = self.dumpWindow(hwnd=dialogHwnd)
            list2 = [item[1] for item in list1]
        else:
            list2 = []
        return list2

    def getWindowText(self, hwnd) -> str:
        # 通过hwnd 获取窗口标题
        text1 = win32gui.GetWindowText(hwnd)
        self.classPrint(f'句柄{hwnd}的窗口标题为 【{text1}】 ')
        return text1

    def getWindowPos(self, hwnd):
        """根据窗口句柄获取窗口的四角坐标

        Args:
            hwnd (int): 十进制的句柄数值

        Returns:
            tuple: 窗口的四角坐标,也可以是控件的四角坐标
        """
        # 根据窗口句柄获取窗口的四角坐标

        x, y, w, h = win32gui.GetWindowRect(hwnd)
        self.classPrint(f'根据窗口句柄获取窗口的四角坐标{(x,y,w,h)}')
        return x, y, w, h

    def getCurrentWinPos(self) -> tuple:
        """获取当前窗口的坐标值

        Returns:
            tuple: 返回坐标元组
        """
        # 获取当前窗口的坐标值，返回坐标元组
        x, y, w, h = self.getWindowPos(self.getNowWinHwnd())
        self.classPrint(f'获取当前窗口的坐标值{(x,y,w,h)}')
        return x, y, w, h

    def getChildHwnds(self):  # TODO 获取父窗口的子窗口句柄们
        self.classPrint(f'')

    def moveAndclick(self, x, y, duration=0.1, remark=''):
        """移动鼠标到指定的坐标点并点击,鼠标默认移动时间为0.1秒

        Args:
            x (int): x坐标点
            y (int): y坐标点
            duration (float, optional): 鼠标移动时长.默认0.1秒.
        """
        self.classPrint(f"移动到%s,%s点击 【{remark}】" % (x, y))
        pag.moveTo(x, y, duration=duration)
        pag.click()

    def moveOffset(self, xOffset, yOffset, duration=0.1):
        # 偏移量移动
        # 相对位置移动，向右100、向上200，鼠标移动过渡时间duration设为0.5秒
        # pag.moveRel(100, -200, duration=duration)
        self.classPrint(f'正x向右,正y向下，x偏移 {xOffset}、y偏移{yOffset}')
        pag.moveRel(xOffset=xOffset, yOffset=yOffset, duration=duration)

    def moveOffsetClick(self, winTitle, xOffset, yOffset):
        """偏移点击

        Args:
            winTitle (str): 窗口标题
            xOffset (int): 偏移量x值
            yOffset (int): 偏移量y值

        Returns:
            _type_: 窗口坐标
        """
        #  先判断窗口名称是不是一样
        if winTitle != self.getWindowText(self.getNowWinHwnd()):
            return False
        # 当前窗口坐标
        winPosition = self.getWindowPos(self.getNowWinHwnd())
        # 偏移移动点击
        self.classPrint(f'基于窗口名称的窗口进行偏移移动点击')
        self.moveAndclick(winPosition[0]+xOffset, winPosition[1]+yOffset)
        return winPosition

    def moveTo(self, x, y, duration=0.1):
        """鼠标移动到x,y 坐标点

        Args:
            x (int): x坐标
            y (int): y坐标
            duration (float, optional): 移动的时间. Defaults to 0.1.
        """
        self.classPrint(f'移动到 {x} {y}')
        pag.moveTo(x, y, duration=duration)

    def pressCtrlC(self):
        # 热键组合
        self.classPrint("输入 Ctrl+C 复制")
        pag.keyDown('ctrl')
        pag.keyDown('c')
        pag.keyUp('c')
        pag.keyUp('ctrl')

    def pressCtrlV(self):
        # 热键组合ctrl+
        self.classPrint("输入 Ctrl+V  粘贴")
        pag.keyDown('ctrl')
        pag.keyDown('v')
        pag.keyUp('v')
        pag.keyUp('ctrl')

    def pressCtrland(self, keyName):
        # 热键组合ctrl+
        self.classPrint("输入Ctrl+%s " % keyName)
        pag.keyDown('ctrl')
        pag.keyDown(keyName)
        pag.keyUp(keyName)
        pag.keyUp('ctrl')

    def press(self, keyName):
        pag.keyDown(keyName)
        pag.keyUp(keyName)

    def pressDlgNoBtn(self, dlgTitle):  # TODO
        keywords = ['否', '不', 'No']
        self.pressDlgBtn(dlgTitle=dlgTitle, btnWords=keywords)

    def pressDlgYesBtn(self, dlgTitle):  # TODO
        keywords = ['是', '确认', '好的', 'OK']
        self.pressDlgBtn(dlgTitle=dlgTitle, btnWords=keywords)

    def pressDlgCancelBtn(self, dlgTitle):  # TODO
        keywords = ['取消', 'Cancel', 'cancel']
        self.pressDlgBtn(dlgTitle=dlgTitle, btnWords=keywords)

    def pressDlgBtn(self, dlgTitle: str, btnWords: list):  # TODO
        btnList = self.dumpWindow(self.getNowWinHwnd(), wantedClass='Button')
        print(btnList, type(btnList))
        if self.getWindowText(self.getNowWinHwnd()) != dlgTitle:
            self.classPrint('窗口标题不一致,不点击')
            return False
        keywords = btnWords
        for item in btnList:
            if checkKeyWord(item[1], keywords):
                self.classPrint('发现关键字按钮', item[1])
                btn1 = item[0]
                # btn1 = btnList[0][0]
                btn1Rect = win32gui.GetWindowRect(btn1)
                print('btn1Rect', btn1Rect)
                x = int((btn1Rect[0]+btn1Rect[2])/2)
                y = int((btn1Rect[1]+btn1Rect[3])/2)
                win32api.SetCursorPos((x, y))
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
                win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
                break

    def picker(self):
        self.classPrint("进入按键脚本录制步步来")
        # 点击后输入步骤名称和动作 TODO

    def rightClick(self):
        # 右键点击
        self.classPrint(f'右键点击{self.getCurPosition()}')
        pag.rightClick()

    def scroll(self, steps=750):
        """ 正为上,负为下, 750约等于一个pageup

        Args:
            steps (int, optional): 翻页步长 Defaults to 750.
        """
        self.classPrint(f'鼠标滚动,正为上,步长{steps}')
        pag.scroll(steps)

    def savePosition(self):
        """保存当前坐标到self.initialPosition中

        """
        # 注释
        self.initialPosition = self.getCurPosition()
        self.classPrint(f'保存当前鼠标坐标{self.initialPosition}')

    def setStartHotkey(self, hotkeyName='ctrl+alt', funcName=lambda x: print(x)):
        # 设置启动热键
        print(funcName, type(funcName))
        colorPrint.red(f'设置启动热键{hotkeyName},绑定函数{funcName}')
        keyboard.add_hotkey(hotkeyName, funcName)
        keyboard.wait('f3')

    def setForegroundWindow(self, hwnd):
        # 将窗口设置为前台显示
        self.classPrint(f'将窗口设置为前台显示{hwnd}')
        win32gui.SetForegroundWindow(hwnd)

    def setWindowPos(self, targetTitle, xPos=600, yPos=300, width=100, height=100):
        """根据窗口标题模糊查找窗口并设置窗口大小
           并且在前台显示!

        Args:
            targetTitle (str): 窗口标题, 支持模糊搜索
            xPos (int, optional): x坐标(绝对坐标). Defaults to 600.
            yPos (int, optional): y坐标(绝对坐标). Defaults to 300.
            width (int, optional): 宽度(左右方向为宽). Defaults to 100.
            height (int, optional): 高度(上下方向为高). Defaults to 100.
        """
        hWndList = []
        win32gui.EnumWindows(lambda hWnd, param: param.append(hWnd), hWndList)
        # print('hWndList',hWndList, type(hWndList))
        for hwnd in hWndList:
            clsname = win32gui.GetClassName(hwnd)
            title = win32gui.GetWindowText(hwnd)
            # print('hwnd, clsname, title',hwnd, clsname, title)
            if (title.find(targetTitle) >= 0):  # 调整目标窗口到坐标(600,300),大小设置为(600,600)
                # win32gui.SetWindowPos(hwnd, win32con.HWND_TOPMOST, 600,300,600,600, win32con.SWP_SHOWWINDOW)
                win32gui.SetWindowPos(
                    hwnd, win32con.HWND_TOP, xPos, yPos, width, height, win32con.SWP_SHOWWINDOW)
                if not Calvin.getNowWinHwnd() == hwnd:
                    self.classPrint(f' 窗口 {title} 需要激活,已激活')
                    win32gui.SetForegroundWindow(hwnd)

    def restorePosition(self):
        # 恢复初始坐标
        pos0 = self.initialPosition
        self.classPrint(f'恢复初始坐标{pos0}')
        self.moveTo(*pos0)

    def revealWindows(self, hwnd):  # TODO 测试还没有用
        # 显示窗口
        self.setForegroundWindow(hwnd=hwnd)

    def userInput(self, tips, title, default=''):
        self.classPrint("等待用户输入")
        userInputStr = pag.prompt(text=tips, title=title, default=default)
        return userInputStr

    def waitWindow(self, wantedHwnd=None, wantedTitle=None, waitTime=10):
        """等待某个满足条件的窗口在前台中出现, 两个条件是或的关系

        Args:
            wantedHwnd (int, optional): 想要查找的窗口的句柄. Defaults to None.
            wantedTitle (str, optional): 想要查找的窗口的标题. Defaults to None.
            waitTime (int, optional): 等待时间,超过这个时间就返回False. Defaults to 10.

        Returns:
            bool: 等待的结果, True or False
        """
        # 等待窗口出现
        timeout = waitTime
        self.classPrint(
            f'等待 wantedHwnd ={wantedHwnd} or wantedTitle={wantedTitle} 窗口出现')
        while waitTime:
            nowWindowHwnd = self.getNowWinHwnd()
            nowWindowTitle = self.getWindowText(nowWindowHwnd)
            if wantedHwnd and nowWindowHwnd == wantedHwnd:
                colorPrint.blue(
                    f'找到{wantedHwnd}窗口{self.getWindowText(wantedHwnd)}')
                return True
            if wantedTitle and nowWindowTitle == wantedTitle:
                colorPrint.blue(
                    f'找到{wantedTitle}窗口{self.getWindowText(wantedHwnd)}')
                return True
            else:
                colorPrint.blue(
                    f'{waitTime} 当前窗口 hwnd {nowWindowHwnd}, 要查找的hwnd为 {wantedHwnd}')
                time.sleep(1)
                waitTime -= 1
        colorPrint.red(
            f'超时 {timeout}秒, 没有找到 wantedHwnd ={wantedHwnd} or wantedTitle={wantedTitle} 窗口')
        return False

    def tripleClick(self):
        # 常用于全选输入框文本
        self.classPrint("鼠标当前位置3击")
        # pyautogui.tripleClick()
        pag.tripleClick(x=None,
                        y=None,
                        interval=0.0,
                        button='left',
                        duration=0.0,
                        tween=pag.linear)

    def typewrite(self, strings):  # FIXME
        """通过复制粘帖的方式输入文字

        Args:
            strings (_type_): 中文和英文都支持
        """
        self.classPrint("输入字符串", strings)
        # pag.typewrite(message=strings, interval=0.2)

        # 此时打开剪贴板，可直接粘贴"Hello world"到剪贴板
        pyperclip.copy(strings)
        self.pressCtrlV()

    def doubleClick(self):
        # 常用于全选输入框文本
        self.classPrint("鼠标当前位置0间隔双击")
        pag.doubleClick(x=None,
                        y=None,
                        interval=0.0,
                        button='left',
                        duration=0.0,
                        tween=pag.linear)

    def chooseOption(self, tips, title, buttonNameList):
        # TODO 下拉选择
        choose = pag.confirm(text="", title="", buttons=['A', 'B', 'C'])
        return choose

    def maximizeWindow(self, handle):  # TODO 最大化窗口
        # 对指定的窗口最大化显示
        pass

    def recordMacro(self):
        """进行基于绝对坐标点击的脚本录制,
        录制的脚本文件名为 ./Macro.txt
        """
        # 脚本默认路径为 本地
        macroPath = './Macro.txt'
        colorPrint.red('录制单次脚本')

        # 返回输入的值（按ok）或者None （按cancel）
        aPosition = self.getCurPosition()
        remarks = pag.prompt(text='请输入注释', title='提示', default='something')
        with open(macroPath, 'a', encoding='utf-8') as f:
            f.write(f'# {remarks}\n')
            f.write(f'Calvin.moveAndclick{str(aPosition)}\n')
            f.write('time.sleep(0.3)\n')
        colorPrint.green(
            f'在 {macroPath} 中写入： Calvin.moveAndclick{str(aPosition)}\n')

    def recordMacro2(self):
        """进行基于窗口偏移点击的脚本录制,
        录制的脚本文件名为 ./MacroOffset.txt
        """
        # 脚本默认路径为 本地
        macroPath = './MacroOffset.txt'
        colorPrint.red('录制脚本,基于窗口起点偏移,记录窗口名字和偏移量')
        # 窗口标题
        winTitle = self.getWindowText(self.getNowWinHwnd())

        # 返回输入的值（按ok）或者None （按cancel）
        aPosition = self.getCurPosition()
        # 当前窗口坐标
        winPosition = self.getCurrentWinPos()
        xRelPos = aPosition[0]-winPosition[0]
        yRelPos = aPosition[1]-winPosition[1]
        remarks = pag.prompt(text='请输入偏移点击的注释', title='提示', default='基于窗口偏移：')
        with open(macroPath, 'a', encoding='utf-8') as f:
            f.write(f'    # {remarks}\n')
            f.write(
                f'    Calvin.moveOffsetClick("{winTitle}",{xRelPos},{yRelPos})\n')
            f.write('    time.sleep(0.3)\n')
        colorPrint.green(
            f'在 {macroPath} 中写入： Calvin.moveOffsetClick("{winTitle}",{xRelPos},{yRelPos})\n')

    def showmsg(self):
        self.classPrint('进行弹窗显示..')

    def screenshot(self, pngPath='../data/shot.png'):
        """屏幕截图, 目前只有截取主屏幕! 暂没有做双显示器的截图

        Args:
            pngPath (str, optional): png文件路径. Defaults to '../data/shot.png'.
            region (tuple, optional): 要截图的区域. Defaults to (1000, 600, 600, 400).
        """
        self.classPrint(
            f'屏幕截图{pngPath}, 坐标 {(0,0,self.screenWidth,self.screenHeight)}')
        pag.screenshot(pngPath, region=(
            0, 0, self.screenWidth, self.screenHeight))

    ''' todo 需求

    窗口操作，最大化，最小化，关闭, 显示在前台


    '''

    @classmethod
    def aOffsetPos(cls, beginPos: tuple, xOffset: int, yOffset: int, rows: int, cols: int) -> list:
        # 注释 起始坐标, x偏移量, y偏移量,行列数
        PosItem = collections.namedtuple(
            "偏移坐标表", ['起始坐标', 'x坐标', 'y坐标', '现行列数'])
        list1 = []
        for i in range(cols):
            for j in range(rows):
                # print(i, j)
                item = PosItem(
                    beginPos, beginPos[0]+xOffset*j, beginPos[1]+yOffset*i, (i, j))
                list1.append(item)
        return list1


if __name__ == '__main__':

    '''
    经典的 mainDemo

    1. 实例化这个类, 取个好听的名字
    2. 打印运行这个类的一些环境信息 
    3. 打印这个类可以获取到的信息,
    4. 执行这个类的一些基本操作

    '''
    # pyautogui.alert(title='脚本执行者', text='脚本即将开始,\n鼠标移动到屏幕左上角(0,0)即可停止脚本.')

    # a = pyautogui.confirm(text='内容文本有真相', title='这个是标题', buttons=[
    #                       'OK1', 'Cancel'])  # OK和Cancel按钮的消息弹窗
    # 返回值为buttons的元素
    # print(a, type(a))

    # a = pyautogui.prompt(text="请输入动作", title="步步来", default='1')
    # pyautogui.confirm('Enter option.', buttons=['A', 'B', 'C'])

    Calvin = ajjl()
    Calvin.setNickname('组态精灵')
    print("屏幕高度", Calvin.screenHeight)
    print("屏幕宽度", Calvin.screenWidth)
    Calvin.savePosition()
    Calvin.screenshot()

    for a in range(10):
        wHwnd = Calvin.getNowWinHwnd()
        print(Calvin.getWindowText(wHwnd))
        time.sleep(0.5)


def test_posGet():
    # 模糊查找和获取坐标
    a = Calvin.FindFuzzyTopWindows('记事本')
    print(getattr(a[0], 'caption'))
    b = Calvin.getWindowPos(getattr(a[0], 'hwnd_py'))
    print(b, type(b))


def test_screenshot():
    # 注释
    # print(arg1, type(arg1))
    area = (0, 0, Calvin.screenWidth, Calvin.screenHeight)
    filePath = f'../data/shot_{myNowTime("%Y%m%d_%H%M%S")}.png'
    Calvin.screenshot(filePath, area)


def test_moveclick(arg1):
    # 注释
    print(arg1, type(arg1))

    Calvin.moveAndclick(827, 508)
    time.sleep(0.5)
    Calvin.moveAndclick(627, 203)


def test_moveOffset():
    # time.sleep(0.5)
    # Ken.moveOffset(10, 100)
    # time.sleep(0.5)
    # Ken.moveOffset(10, 10)
    # time.sleep(0.5)
    Calvin.moveOffset(200, 10)


def test_scrollDemo():
    # Ken.scroll(1000)
    steps = 760
    Calvin.scroll(-steps)
    time.sleep(1)
    Calvin.scroll(steps)


def listMove(arg1=1):
    # 注释
    print(arg1, type(arg1))

    list1 = Calvin.aOffsetPos((1, 1), 100, 120, 4, 5)
    for item in list1:
        xPos = getattr(item, 'x坐标')
        yPos = getattr(item, 'y坐标')
        Calvin.moveTo(xPos, yPos)

    Calvin.getWindowText(Calvin.getNowWinHwnd())

    Calvin.restorePosition()


def demo3():
    runningFlag = 0  # 运行标志位

    def test_a():
        global runningFlag
        if runningFlag == 0:
            runningFlag = 1
        else:
            print('aaa进行中....')
            aPosition = Calvin.getCurPosition()
            with open('./Macro.txt', 'a', encoding='utf-8') as f:
                f.write(f'Ken.moveAndclick{str(aPosition)}\n')
                f.write('time.sleep(1)\n')
            # time.sleep(2)

            runningFlag = 0
            colorPrint.green('aaa运行结束!')

    def test(x):
        print(x)
        aPosition = Calvin.getCurPosition()
        macroPath = './Macro.txt'
        with open(macroPath, 'a', encoding='utf-8') as f:
            f.write(f'Ken.moveAndclick{str(aPosition)}\n')
            f.write('time.sleep(1)\n')

        colorPrint.green(
            f'在 {macroPath} 中写入： Ken.moveAndclick{str(aPosition)}\n')

    # 绑定一个热键和一个执行事件, 即按了就执行test_a
    keyboard.add_hotkey('f2', test_a)
    # 按f1输出aaa
    keyboard.add_hotkey('ctrl+alt', test, args=('record one....',))
    # 按ctrl+alt输出b
    keyboard.wait('f3')
    colorPrint.purple('程序完全退出.....')
    # wait里也可以设置按键，说明当按到该键时结束
