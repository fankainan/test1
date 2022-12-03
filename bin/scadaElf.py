import pyautogui as pag
import time
import sys
import os
import collections
import win32gui
import keyboard
import time
from ajjlPython import ajjl

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

print('获取当前工作目录路径', os.getcwd())  # 获取当前工作目录路径
print("初始化工作目录,避免在CLI中出现相对路径的运行错误问题")
dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
os.chdir(dirname)
print(f"修改工作目录为 {dirname}")

# os.chdir(os.path.dirname(__file__))
sys.path.append('../lib')
from mytools import basicClass, colorPrint  # NOQA: E402
from mytools import myNowTime  # NOQA: E402


# 版本说明： 2022.09.09 新建
# 功能说明： 组态操作类
# 备注说明：
# 环境要求： 
# 设备要求： win10测试通过


class scada_elf(ajjl):


    def __init__(self):
        super().__init__()
        self.instanceName = '组态精灵: '

    def testhi(self, arg1):
        # TODO 测试
        print(arg1, type(arg1))
        self.classPrint(f'测试')
    def runPlatf(self, arg1):
        # TODO 运行平台
        print(arg1, type(arg1))
        self.classPrint(f'运行平台')
    

class hmiEUT(basicClass):

    def getPnCode(self, arg1):
        # TODO 获取pn妈
        print(arg1, type(arg1))
        self.classPrint(f'获取pn妈')
        
    def checkPnCode(self, arg1):
        # TODO 核对pn码
        print(arg1, type(arg1))
        self.classPrint(f'核对pn码')
        
        

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
