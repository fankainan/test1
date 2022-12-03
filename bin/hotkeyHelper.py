# -*- coding: utf-8 -*-

import win32con
import ctypes
import ctypes.wintypes
import threading
from ajjlPython import ajjl

Ken = ajjl()
Ken.setNickname('tb自动复制型号')


class hotkeyHelper(threading.Thread):
    vkDict = {8: 'WIN',
              112: 'F1',
              113: 'F2',
              114: 'F3',
              115: 'F4',
              116: 'F5',
              117: 'F6',
              118: 'F7',
              119: 'F8',
              120: 'F9',
              121: 'F10'}

    def __init__(self, func, args, name=''):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.name = name
        self.user32 = ctypes.windll.user32
        # self.regStartKey(win32con.MOD_WIN, win32con.VK_F3) 不能在这里注册，会导致热键没有反应，不知道为什么，可能是需要回调

    # 执行代码，附加注册开始热键
    def run(self, combination_key1, combination_key2):
        print("\n***start of "+str(self.name)+"***\n")
        self.regStartKey(combination_key1, combination_key2)
        while(True):
            try:
                msg = ctypes.wintypes.MSG()
                if self.user32.GetMessageA(ctypes.byref(msg), None, 0, 0) != 0:
                    if msg.message == win32con.WM_HOTKEY:
                        if msg.wParam == 99:  # exit
                            print('检测到停止热键！程序结束，注销热键')
                            # 要记得释放热键
                            del msg
                            self.user32.UnregisterHotKey(None, 98)
                            self.user32.UnregisterHotKey(None, 99)
                            return
                        elif msg.wParam == 98:  # 开始
                            # print('F9 98')
                            print('----------------\n检测到开始热键！动作开始\n-----------------')
                            self.res = self.func(*self.args)
                    # TranslateMessage函数将虚拟键消息转换成字符消息
                    # TranslateMessage函数将键盘消息转化,DispatchMessage函数将消息传给窗体函数去处理.
                    self.user32.TranslateMessage(ctypes.byref(msg))
                    self.user32.DispatchMessageA(ctypes.byref(msg))
            except Exception:
                print('execute error occured')
            # finally:
            #     print('finally execute')

            print("\n***end of "+str(self.name)+"***\n")

    def regStartKey(self, combination_key1=win32con.MOD_WIN, combination_key2=win32con.VK_F8):
        print('开始注册热键ing......')
        # 注册开始热键组合
        if not self.user32.RegisterHotKey(None, 98, combination_key1, combination_key2):
            # start program
            print("Unable to register id", 98)
        else:
            print('注册 开始热键{}+{} registe ok'.format(hotkeyHelper.vkDict.get(combination_key1),hotkeyHelper.vkDict.get(combination_key2)))

        # 注册停止热键组合
        if not self.user32.RegisterHotKey(None, 99, win32con.MOD_WIN, win32con.VK_F10):
            # exit program
            print("Unable to register id", 99)
        else:
            print('注册 停止热键{}+{} registe ok'.format(hotkeyHelper.vkDict.get(win32con.MOD_WIN),hotkeyHelper.vkDict.get(win32con.VK_F10)))


def action(repeatTime):
    # Ken.doubleClick()
    for i in range(repeatTime):
        # x, y = Ken.getCurPosion()
        # Ken.moveAndclick(x+80, y)
        # Ken.moveAndclick(x, y)
        # Ken.press('home')
        Ken.doubleClick()
        name = rnd_name()

        pyperclip.copy(name)
        Ken.pressCtrlV()
        x, y = Ken.getCurPosion()
        Ken.moveTo(x, y+19)



# -*- coding:utf-8 -*-
import random as r
import pyperclip

a1 = [
    '赵', '赵', '赵', '赵', '赵', '赵', '赵', '赵', '赵', '赵', '赵', '赵', '赵', '钱', '钱',
    '钱', '钱', '钱', '钱', '孙', '孙', '孙', '孙', '孙', '孙', '孙', '李', '李', '李', '李',
    '李', '李', '李', '李', '周', '吴', '吴', '吴', '吴', '吴', '吴', '郑', '郑', '郑', '郑',
    '郑', '郑', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '蒋', '蒋', '沈', '沈', '沈', '沈',
    '沈', '沈', '韩', '韩', '韩', '韩', '韩', '韩', '杨', '朱', '秦', '尤', '许', '许', '许',
    '许', '许', '许', '何', '吕', '吕', '吕', '吕', '吕', '吕', '吕', '施', '张', '张', '张',
    '张', '张', '张', '张', '张', '张', '孔', '孔', '孔', '曹', '曹', '曹', '曹', '曹', '严',
    '华', '金', '金', '金', '金', '魏', '魏', '魏', '魏', '陶', '姜', '戚', '谢', '邹', '喻',
    '柏', '水', '窦', '章', '云', '苏', '苏', '苏', '苏', '苏', '苏', '苏', '潘', '葛', '奚',
    '范', '彭', '彭', '彭', '彭', '彭', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花',
    '方', '方', '方', '方', '方', '方', '方', '俞', '任', '袁', '柳', '酆', '鲍', '史', '唐',
    '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '罗', '罗', '毕', '郝',
    '邬', '安', '常', '乐', '于', '于', '于', '时', '傅', '傅', '傅', '傅', '皮', '卞', '齐',
    '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹', '姚', '邵',
    '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '戴', '戴',
    '宋', '茅', '庞', '熊', '纪', '舒', '屈', '项', '祝', '董', '梁', '欧阳'
]
english_first_name = [
    'Smith', 'Jones ', 'Williams ', 'Taylor ', 'Brown ', 'Davies ', 'Evans ',
    'Wilson ', 'Thomas ', 'Johnson ', 'Roberts ', 'Robinson ', 'Thompson ',
    'Wright ', 'Walker ', 'White ', 'Edwards ', 'Hughes ', 'Green ', 'Hall ',
    'Lewis ', 'Harris ', 'Clarke ', 'Patel ', 'Jackson ', 'Smith ', 'Brown ',
    'Wilson ', 'Campbell ', 'Stewart ', 'Thomson ', 'Robertson ', 'Anderson ',
    'Macdonald ', 'Scott ', 'Reid ', 'Murray ', 'Taylor ', 'Clark ', 'Ross ',
    'Watson ', 'Morrison ', 'Paterson ', 'Young ', 'Mitchell ', 'Walker ',
    'Fraser ', 'Miller ', 'McDonald ', 'Gray ', 'Henderson ', 'Hamilton ',
    'Johnston ', 'Duncan ', 'Graham ', 'Ferguson ', 'Kerr ', 'Davidson ',
    'Bell ', 'Cameron ', 'Kelly ', 'Martin ', 'Hunter ', 'Allan ',
    'Mackenzie ', 'Grant ', 'Simpson ', 'MacKay ', 'McLean ', 'MacLeod ',
    'Black ', 'Russell ', 'Marshall ', 'Wallace ', 'Gibson ', 'Smith  ',
    'Johnson ', 'Williams ', 'Jones ', 'Brown ', 'Davis ', 'Miller ',
    'Wilson ', 'Moore ', 'Taylor ', 'Anderson ', 'Thomas ', 'Jackson ',
    'White ', 'Harris ', 'Martin ', 'Thompson ', 'Garcia ', 'Martinez ',
    'Robinson ', 'Clark ', 'Rodriguez ', 'Lewis ', 'Lee ', 'Walker ', 'Hall ',
    'Allen ', 'Young ', 'Hernandez ', 'King ', 'Wright ', 'Lopez ', 'Hill ',
    'Scott ', 'Green ', 'Adams ', 'Baker ', 'Gonzalez ', 'Nelson ', 'Carter ',
    'Mitchell ', 'Perez ', 'Roberts ', 'Turner ', 'Phillips ', 'Campbell ',
    'Parker ', 'Evans ', 'Edwards ', 'Collins ', 'Stewart ', 'Sanchez ',
    'Morris ', 'Rogers ', 'Reed ', 'Cook ', 'Morgan ', 'Bell ', 'Murphy ',
    'Bailey ', 'Rivera ', 'Cooper ', 'Richardson ', 'Cox ', 'Howard ', 'Ward ',
    'Torres ', 'Peterson ', 'Gray ', 'Ramirez ', 'James ', 'Watson ',
    'Brooks ', 'Kelly ', 'Sanders ', 'Price ', 'Bennett ', 'Wood ', 'Barnes ',
    'Ross ', 'Henderson ', 'Coleman ', 'Jenkins ', 'Perry ', 'Powell ',
    'Long ', 'Patterson ', 'Hughes ', 'Flores ', 'Washington ', 'Butler ',
    'Simmons ', 'Foster'
]
english_last_name = [
    'Smith', 'Jones ', 'Williams ', 'Taylor ', 'Brown ', 'Davies ', 'Evans ',
    'Wilson ', 'Thomas ', 'Johnson ', 'Roberts ', 'Robinson ', 'Thompson ',
    'Wright ', 'Walker ', 'White ', 'Edwards ', 'Hughes ', 'Green ', 'Hall ',
    'Lewis ', 'Harris ', 'Clarke ', 'Patel ', 'Jackson ', 'Smith ', 'Brown ',
    'Wilson ', 'Campbell ', 'Stewart ', 'Thomson ', 'Robertson ', 'Anderson ',
    'Macdonald ', 'Scott ', 'Reid ', 'Murray ', 'Taylor ', 'Clark ', 'Ross ',
    'Watson ', 'Morrison ', 'Paterson ', 'Young ', 'Mitchell ', 'Walker ',
    'Fraser ', 'Miller ', 'McDonald ', 'Gray ', 'Henderson ', 'Hamilton ',
    'Johnston ', 'Duncan ', 'Graham ', 'Ferguson ', 'Kerr ', 'Davidson ',
    'Bell ', 'Cameron ', 'Kelly ', 'Martin ', 'Hunter ', 'Allan ',
    'Mackenzie ', 'Grant ', 'Simpson ', 'MacKay ', 'McLean ', 'MacLeod ',
    'Black ', 'Russell ', 'Marshall ', 'Wallace ', 'Gibson ', 'Smith  ',
    'Johnson ', 'Williams ', 'Jones ', 'Brown ', 'Davis ', 'Miller ',
    'Wilson ', 'Moore ', 'Taylor ', 'Anderson ', 'Thomas ', 'Jackson ',
    'White ', 'Harris ', 'Martin ', 'Thompson ', 'Garcia ', 'Martinez ',
    'Robinson ', 'Clark ', 'Rodriguez ', 'Lewis ', 'Lee ', 'Walker ', 'Hall ',
    'Allen ', 'Young ', 'Hernandez ', 'King ', 'Wright ', 'Lopez ', 'Hill ',
    'Scott ', 'Green ', 'Adams ', 'Baker ', 'Gonzalez ', 'Nelson ', 'Carter ',
    'Mitchell ', 'Perez ', 'Roberts ', 'Turner ', 'Phillips ', 'Campbell ',
    'Parker ', 'Evans ', 'Edwards ', 'Collins ', 'Stewart ', 'Sanchez ',
    'Morris ', 'Rogers ', 'Reed ', 'Cook ', 'Morgan ', 'Bell ', 'Murphy ',
    'Bailey ', 'Rivera ', 'Cooper ', 'Richardson ', 'Cox ', 'Howard ', 'Ward ',
    'Torres ', 'Peterson ', 'Gray ', 'Ramirez ', 'James ', 'Watson ',
    'Brooks ', 'Kelly ', 'Sanders ', 'Price ', 'Bennett ', 'Wood ', 'Barnes ',
    'Ross ', 'Henderson ', 'Coleman ', 'Jenkins ', 'Perry ', 'Powell ',
    'Long ', 'Patterson ', 'Hughes ', 'Flores ', 'Washington ', 'Butler ',
    'Simmons ', 'Foster'
]
a2 = [
    '晨', '轩', '清', '睿', '宝', '涛', '华', '国', '亮', '新', '凯', '志', '明', '伟', '嘉',
    '东', '洪', '建', '文', '子', '云', '杰', '兴', '友', '才', '振', '辰', '航', '达', '鹏',
    '宇', '衡', '佳', '强', '宁', '丰', '波', '森', '学', '民', '永', '翔', '鸿', '海', '飞',
    '义', '生', '凡', '连', '良', '乐', '勇', '辉', '龙', '川', '宏', '谦', '锋', '双', '霆',
    '玉', '智', '增', '名', '进', '德', '聚', '军', '兵', '忠', '廷', '先', '江', '昌', '政',
    '君', '泽', '超', '信', '腾', '恒', '礼', '元', '磊', '阳', '月', '士', '洋', '欣', '升',
    '恩', '迅', '科', '富', '函', '业', '胜', '震', '福', '瀚', '瑞', '朔', '津', '韵', '荣',
    '为', '诚', '斌', '广', '庆', '成', '峰', '可', '健', '英', '功', '冬', '锦', '立', '正',
    '禾', '平', '旭', '同', '全', '豪', '源', '安', '顺', '帆', '向', '雄', '材', '利', '希',
    '风', '林', '奇', '易', '来', '咏', '岩', '启', '坤', '昊', '朋', '和', '纪', '艺', '昭',
    '映', '威', '奎', '帅', '星', '春', '营', '章', '高', '伦', '庭', '蔚', '益', '城', '牧',
    '钊', '刚', '洲', '家', '晗', '迎', '罡', '浩', '景', '珂', '策', '皓', '栋', '起', '棠',
    '登', '越', '盛', '语', '钧', '亿', '基', '理', '采', '备', '纶', '献', '维', '瑜', '齐',
    '凤', '毅', '谊', '贤', '逸', '卫', '万', '臻', '儒', '钢', '洁', '霖', '隆', '远', '聪',
    '耀', '誉', '继', '珑', '哲', '岚', '舜', '钦', '琛', '金', '彰', '亭', '泓', '蒙', '祥',
    '意', '鑫', '朗', '晟', '晓', '晔', '融', '谋', '宪', '励', '璟', '骏', '颜', '焘', '垒',
    '尚', '镇', '济', '雨', '蕾', '韬', '选', '议', '曦', '奕', '彦', '虹', '宣', '蓝', '冠',
    '谱', '泰', '泊', '跃', '韦', '怡', '骁', '俊', '沣', '骅', '歌', '畅', '与', '圣', '铭',
    '溓', '滔', '溪', '巩', '影', '锐', '展', '笑', '祖', '时', '略', '敖', '堂', '崊', '绍',
    '崇', '悦', '邦', '望', '尧', '珺', '然', '涵', '博', '淼', '琪', '群', '驰', '照', '传',
    '诗', '靖', '会', '力', '大', '山', '之', '中', '方', '仁', '世', '梓', '竹', '至', '充',
    '亦', '丞', '州', '言', '佚', '序', '宜', '坤'
]


def rnd_name():
    a3 = a2
    print("输出结果：")

    choose = r.randint(1, 99)
    print("choose==", choose)
    if choose > 0:
        if choose > 30:  # 输出三个子
            name = r.choice(a1) + r.choice(a2) + r.choice(a3)
        else:  # 输出二个子
            name = r.choice(a1) + r.choice(a2)
    # if choose<=30:
    # name=r.choice(english_first_name)+r.choice(english_last_name)
    print(name)
    return name


if __name__ == '__main__':
    name = rnd_name()
# f=open("A.txt","a")
# f.write(name+'\n')
    pyperclip.copy(name)
    # pyperclip.copy(name.decode('utf-8'))







if __name__ == "__main__":
    # 要能自定义执行的动作函数
    myHotKey = hotkeyHelper(func=action, args=(60,), name="按键精灵Python版")
    # 要能自定义热键，开始和结束
    myHotKey.run(win32con.MOD_WIN, win32con.VK_F3)
    # myHotKey.join() 没有start就没有join
