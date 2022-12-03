# -*- coding: utf-8 -*-
from shutil import copyfile
import sys
import time
import os
import filecmp






# 版本说明：2022.01.28新建,
# 功能说明： 核对lib目录中的py文件是否跟系统lib中的文件是否一致,如果不一致就复制系统中的文件,以系统lib中的文件为准
# 备注说明： 用于更新[用于发布的lib]中的文件
# 环境要求：windows系统
# 设备要求：无

def myPrint(var, all_var=locals()):
    """打印变量名和变量值
    Args:
        var (any): 任何变量均可以
        all_var (any, optional): 所有变量. Defaults to locals().
    """
    try:
        varName = [var_name for var_name in all_var if all_var[var_name] is var][0]
    except Exception:
        print('myPrint 参数error', var)
    else:
        nowTime = time.strftime('%Y-%m-%d %H:%M:%S',
                                time.localtime(time.time()))+" "
        print(nowTime, varName.rjust(10), '=', var, type(var))


# 确认当前目录是lib,如果不是lib就不能使用本程序
fileDir = os.path.dirname(__file__)  # 获取当前文件的完整目录
try:
    fatherDirName = os.path.split(fileDir)[-1]  # 采用-1数组坐标这样的方法不是很好
except Exception:
    myPrint('error')
else:
    myPrint(fatherDirName)
    if fatherDirName != 'lib':
        print('父目录不是lib, 同步功能不能用')
        sys.exit()
    else:
        print('父目录是lib, 开始核对文件是否一致')


sourcePath = r"C:\Users\Mr.Dai\AppData\Local\Programs\Python\Python37\Lib\\"
for root, dirs, files in os.walk(fileDir):
    myPrint(root)
    myPrint(files)  # 获取到文件名list
    break

files.remove(os.path.basename(__file__))  # 去掉本身

copyCount = 0  # 同步成功
ngCount = 0  # 同步失败
okCount = 0  # 无需同步

for file in files:
    file1Path = os.path.join(root, file)
    file2Path = os.path.join(sourcePath, file)
    if os.path.isfile(file1Path) and os.path.isfile(file2Path):
        if not (filecmp.cmp(f1=file1Path, f2=file2Path)):
            print("发现文件异常")
            mtime = os.stat(file1Path).st_mtime
            file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
            print("{0} 修改时间是: {1}".format(file1Path, file_modify_time))

            mtime = os.stat(file2Path).st_mtime
            file_modify_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(mtime))
            print("{0} 修改时间是: {1}".format(file2Path, file_modify_time))

            print(f"复制{file2Path} 到 {file1Path}")
            copyfile(file2Path, file1Path)
            copyCount += 1
        else:
            print(file.rjust(17), '核对通过')
            okCount += 1
    else:
        print(f'{sourcePath} 中无 {file}')
        ngCount += 1

print('最终结果↓'.ljust(50,'*'))
print(f'本目录文件数 {len(files)}, 成功同步 {copyCount}, 不需同步 {okCount}, 同步失败 {ngCount}')
sys.exit()
