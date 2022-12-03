from itertools import zip_longest
import os
import sys
from ajjlPython import ajjl
import keyboard
import time
from scadaElf import scada_elf


# 方式1
# BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
# os.chdir(os.path.dirname(__file__))
# sys.path.append('../lib')


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


Calvin = scada_elf()


def scadaAuto():  # 在这里写你的脚本动作

    hwnd1 = Calvin.FindFuzzyTopWindows('记事本')
    if hwnd1:

        time.sleep(5)
        Calvin.waitWindow(hwnd1)
    else:
        colorPrint.red(f'没有找到{hwnd1}')


funcFlag = 1  # 波特率 标记位
ZLGSflag = 1  # 资料格式 标记位
COMflag = 1 # com口 标记位

def scadaAuto2():  # 在这里写你的脚本动作
    global funcFlag
    Calvin.savePosition()
    # 参数通讯
    Calvin.moveAndclick(256, 859)

    Calvin.rightClick()
    # 设置通讯参数
    Calvin.moveAndclick(344, 819)
    # 下拉箭头
    Calvin.moveAndclick(946, 589)
    time.sleep(0.3)
    # 选择波特率
    chooseBR(funcFlag)
    # # 确定
    # Calvin.moveAndclick(1054, 665)
    # time.sleep(0.3)
    Calvin.restorePosition()


def switchFunc():
    global funcFlag
    funcFlag += 1
    print(f'目前动作为{funcFlag}')
    if funcFlag == 8:
        funcFlag = 1


def chooseBR(br):

    print('切换动作', br)
    if br == 1:  # 2400
        # 2400
        Calvin.moveAndclick(863, 612)
        time.sleep(0.3)
    if br == 2:
        # 4800
        Calvin.moveAndclick(868, 628)
        time.sleep(0.3)
    if br == 3:
        # 9600
        Calvin.moveAndclick(867, 641)
        time.sleep(0.3)
    if br == 4:
        # 19200
        Calvin.moveAndclick(876, 658)
        time.sleep(0.3)
    if br == 5:
        # 38400
        Calvin.moveAndclick(880, 674)
        time.sleep(0.3)
        pass
    if br == 6:
        # 57600
        Calvin.moveAndclick(864, 688)
        time.sleep(0.3)
        pass
    if br == 7:
        # 115200
        Calvin.moveAndclick(867, 696)
        time.sleep(0.3)


startKey2 = 'ctrl+1'
switchKey = 'f9'
endKey = 'f3'
recordKey = 'ctrl+alt'
startMsg = f'{Calvin.instanceName}开始运行..\n.按 {startKey2} 开始执行动作 \n 按{recordKey}记录当前鼠标点'
colorPrint.blue(startMsg, '通知')
Calvin.alert(startMsg, '通知')
# keyboard.add_hotkey(startKey, scadaAuto)
keyboard.add_hotkey(startKey2, scadaAuto2)
keyboard.add_hotkey(switchKey, switchFunc)
keyboard.add_hotkey(recordKey, Calvin.recordMacro)
keyboard.wait(endKey)
colorPrint.purple('程序完全退出.....')
# Calvin.alert(f'{Calvin.instanceName}运行结束','通知')
