import os
import sys
from ajjlPython import ajjl
import keyboard
import time
from scadaElf import scada_elf


# 方式1
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
os.chdir(os.path.dirname(__file__))
sys.path.append('../lib')


# 方式2
print('获取当前工作目录路径', os.getcwd())  # 获取当前工作目录路径
print("初始化工作目录,避免在CLI中出现相对路径的运行错误问题")
dirname, filename = os.path.split(os.path.abspath(sys.argv[0]))
os.chdir(dirname)
print(f"修改工作目录为 {dirname}")
sys.path.append('../lib')

# 以下为自己定义的库，在lib目录中
from mytools import myLog, myNowTime, readJsonFile, writeJsonFile  # NOQA: E402
from mytools import init_chdir  # NOQA: E402
from mytools import basicClass, getNowTime  # NOQA: E402
from mytools import colorPrint  # NOQA: E402

# 版本说明： 2022.09.08 优化lib的导入方式
# 功能说明： 组态精灵的运行入口
# 备注说明：
# 环境要求： python3 \ windows32or64
# 设备要求：


Calvin = ajjl()


def test_getPos():
    # None
    Calvin.moveAndclick(-560, -1351)
    time.sleep(0.3)
    # 退出
    Calvin.moveAndclick(776, 16)
    time.sleep(0.3)
    # None
    Calvin.moveAndclick(878, 518)
    time.sleep(0.3)
    # None
    Calvin.moveAndclick(580, 461)
    time.sleep(0.3)


def test_demo():
    # 注释
    print('hello world')
    # 第一点
    Calvin.moveAndclick(142, 178)
    time.sleep(0.3)
    # 第二点
    Calvin.moveAndclick(331, 176)
    time.sleep(0.3)
    # 33333
    Calvin.moveAndclick(144, 321)
    time.sleep(0.3)
    # 4
    Calvin.moveAndclick(336, 313)
    time.sleep(0.3)

    biaoti = ''
    timeoutCount = 20
    while biaoti != '记事本' and timeoutCount > 1:
        jubin = Calvin.getNowWinHwnd()
        biaoti = Calvin.getWindowText(jubin)
        time.sleep(1)
        timeoutCount = timeoutCount - 1
    if timeoutCount == 1:
        print('超时啦~~')
    else:

        # 保存
        Calvin.moveAndclick(1242, 585)
        time.sleep(0.3)

    Calvin.rightClick()


def scadaAuto():  # 在这里写你的脚本动作
    hwnd1 = Calvin.FindFuzzyTopWindows('记事本')
    if hwnd1:

        time.sleep(5)
        Calvin.waitWindow(hwnd1)
    else:
        colorPrint.red(f'没有找到{hwnd1}')


startKey = 'f8'
endKey = 'f3'
recordKey = 'ctrl+alt'
startMsg = f'{Calvin.instanceName}开始运行..\n.按 {startKey} 开始执行动作 \n 按{recordKey}记录当前鼠标点'
colorPrint.blue(startMsg, '通知')
Calvin.alert(startMsg, '通知')
keyboard.add_hotkey(startKey, test_getPos)
keyboard.add_hotkey(recordKey, Calvin.recordMacro2)
keyboard.wait(endKey)
colorPrint.purple('程序完全退出.....')
# Calvin.alert(f'{Calvin.instanceName}运行结束','通知')


