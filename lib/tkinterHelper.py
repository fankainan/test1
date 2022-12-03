# -*- coding: utf-8 -*-
# author:dzy
import tkinter as tk  # 使用Tkinter前需要先导入
from mytools import basicClass, init_chdir
from mytools import getNowTime
from tkinter import END
from tkinter.filedialog import askopenfile
import tkinter.messagebox
from tkinter import simpledialog
from tkinter import StringVar
from tkinter import ttk


# 为了日历控件Calendar类用的
import calendar
import tkinter.font as tkFont


# 版本说明： 2022.04.12 将mytoplevel继承tk_helper
# 2022.04.12, 增加一些kwargs
# 2022.01.04 修改icon设置方法 2021.04.24增加resizeFull，2021.03.15 新建
# 功能说明： 作为tkinter自封的库，把一些常用功能都封装好，便于之后的使用
# 备注说明：
# 环境要求：
# 设备要求：

version = '1.3.2 2022.04.12'
mydatetime = calendar.datetime.datetime
mytimedelta = calendar.datetime.timedelta


class Calendar:
    def __init__(self, fatherWidget, point=None):

        self.Cwindow = tk.Toplevel(master=fatherWidget)
        self.Cwindow.withdraw()
        self.Cwindow.attributes('-topmost', True)
        self.Cwindow.transient(master=fatherWidget)  # 窗口只置顶root之上
        fwday = calendar.SUNDAY
        year = mydatetime.now().year
        month = mydatetime.now().month
        locale = None
        sel_bg = '#ecffc4'
        sel_fg = '#05640e'
        self._date = mydatetime(year, month, 1)  # 每月第一日
        self._selection = None  # 设置为未选中日期
        self.G_Frame = ttk.Frame(self.Cwindow)
        self._cal = self.__get_calendar(locale, fwday)
        self.__setup_styles()        # 创建自定义样式
        self.__place_widgets()       # pack/grid 小部件
        self.__config_calendar()     # 调整日历列和安装标记
        # 配置画布和正确的绑定，以选择日期。
        self.__setup_selection(sel_bg, sel_fg)
        # 存储项ID，用于稍后插入。
        self._items = [self._calendar.insert(
            '', 'end', values='') for _ in range(6)]
        # 在当前空日历中插入日期
        self._update()
        self.G_Frame.pack(expand=1, fill='both')
        self.Cwindow.overrideredirect(1)
        self.Cwindow.update_idletasks()
        width, height = self.Cwindow.winfo_reqwidth(), self.Cwindow.winfo_reqheight()
        self.height = height
        if point:
            x, y = point[0], point[1]
        else:
            x, y = (self.Cwindow.winfo_screenwidth() - width) / \
                2, (self.Cwindow.winfo_screenheight() - height)/2
        self.Cwindow.geometry('%dx%d+%d+%d' % (width, height, x, y))  # 窗口位置居中
        # self.Cwindow.after(300, self._main_judge)
        self.Cwindow.deiconify()
        self.Cwindow.focus_set()
        self.Cwindow.wait_window()  # 这里应该使用wait_window挂起窗口，如果使用mainloop,可能会导致主程序很多错误

    def __get_calendar(self, locale, fwday):
        if locale is None:
            return calendar.TextCalendar(fwday)
        else:
            return calendar.LocaleTextCalendar(fwday, locale)

    def __setitem__(self, item, value):
        if item in ('year', 'month'):
            raise AttributeError("attribute '%s' is not writeable" % item)
        elif item == 'selectbackground':
            self._canvas['background'] = value
        elif item == 'selectforeground':
            self._canvas.itemconfigure(self._canvas.text, item=value)
        else:
            self.G_Frame.__setitem__(self, item, value)

    def __getitem__(self, item):
        if item in ('year', 'month'):
            return getattr(self._date, item)
        elif item == 'selectbackground':
            return self._canvas['background']
        elif item == 'selectforeground':
            return self._canvas.itemcget(self._canvas.text, 'fill')
        else:
            r = ttk.tclobjs_to_py({item: ttk.Frame.__getitem__(self, item)})
            return r[item]

    def __setup_styles(self):
        # 自定义TTK风格
        style = ttk.Style(self.Cwindow)

        def arrow_layout(dir): return (
            [('Button.focus', {'children': [('Button.%sarrow' % dir, None)]})]
        )
        style.layout('L.TButton', arrow_layout('left'))
        style.layout('R.TButton', arrow_layout('right'))

    def __place_widgets(self):
        # 标头框架及其小部件
        Input_judgment_num = self.Cwindow.register(
            self.Input_judgment)  # 需要将函数包装一下，必要的
        hframe = ttk.Frame(self.G_Frame)
        gframe = ttk.Frame(self.G_Frame)
        bframe = ttk.Frame(self.G_Frame)
        hframe.pack(in_=self.G_Frame, side='top', pady=5, anchor='center')
        gframe.pack(in_=self.G_Frame, fill=tk.X, pady=5)
        bframe.pack(in_=self.G_Frame, side='bottom', pady=5)
        lbtn = ttk.Button(hframe, style='L.TButton', command=self._prev_month)
        lbtn.grid(in_=hframe, column=0, row=0, padx=12)
        rbtn = ttk.Button(hframe, style='R.TButton', command=self._next_month)
        rbtn.grid(in_=hframe, column=5, row=0, padx=12)
        self.CB_year = ttk.Combobox(hframe, width=5, values=[str(year) for year in range(mydatetime.now(
        ).year, mydatetime.now().year-11, -1)], validate='key', validatecommand=(Input_judgment_num, '%P'))
        self.CB_year.current(0)
        self.CB_year.grid(in_=hframe, column=1, row=0)
        self.CB_year.bind(
            '<KeyPress>', lambda event: self._update(event, True))
        self.CB_year.bind("<<ComboboxSelected>>", self._update)
        tk.Label(hframe, text='年', justify='left').grid(
            in_=hframe, column=2, row=0, padx=(0, 5))
        self.CB_month = ttk.Combobox(hframe, width=3, values=[
            '%02d' % month for month in range(1, 13)], state='readonly')
        self.CB_month.current(mydatetime.now().month - 1)
        self.CB_month.grid(in_=hframe, column=3, row=0)
        self.CB_month.bind("<<ComboboxSelected>>", self._update)
        tk.Label(hframe, text='月', justify='left').grid(
            in_=hframe, column=4, row=0)
        # 日历部件
        self._calendar = ttk.Treeview(
            gframe, show='', selectmode='none', height=7)
        self._calendar.pack(expand=1, fill='both', side='bottom', padx=5)
        ttk.Button(bframe, text="确 定", width=6, command=lambda: self._exit(
            True)).grid(row=0, column=0, sticky='ns', padx=20)
        ttk.Button(bframe, text="取 消", width=6, command=self._exit).grid(
            row=0, column=1, sticky='ne', padx=20)
        tk.Frame(self.G_Frame, bg='#565656').place(
            x=0, y=0, relx=0, rely=0, relwidth=1, relheigh=2/200)
        tk.Frame(self.G_Frame, bg='#565656').place(
            x=0, y=0, relx=0, rely=198/200, relwidth=1, relheigh=2/200)
        tk.Frame(self.G_Frame, bg='#565656').place(
            x=0, y=0, relx=0, rely=0, relwidth=2/200, relheigh=1)
        tk.Frame(self.G_Frame, bg='#565656').place(
            x=0, y=0, relx=198/200, rely=0, relwidth=2/200, relheigh=1)

    def __config_calendar(self):
        # cols = self._cal.formatweekheader(3).split()
        cols = ['日', '一', '二', '三', '四', '五', '六']
        self._calendar['columns'] = cols
        self._calendar.tag_configure('header', background='grey90')
        self._calendar.insert('', 'end', values=cols, tag='header')
        # 调整其列宽
        font = tkFont.Font()
        maxwidth = max(font.measure(col) for col in cols)
        for col in cols:
            self._calendar.column(col, width=maxwidth, minwidth=maxwidth,
                                  anchor='center')

    def __setup_selection(self, sel_bg, sel_fg):
        def __canvas_forget(evt):
            canvas.place_forget()
            self._selection = None

        self._font = tkFont.Font()
        self._canvas = canvas = tk.Canvas(
            self._calendar, background=sel_bg, borderwidth=0, highlightthickness=0)
        canvas.text = canvas.create_text(0, 0, fill=sel_fg, anchor='w')
        canvas.bind('<Button-1>', __canvas_forget)
        self._calendar.bind('<Configure>', __canvas_forget)
        self._calendar.bind('<Button-1>', self._pressed)

    def _build_calendar(self):
        year, month = self._date.year, self._date.month
        header = self._cal.formatmonthname(year, month, 0)
        # 更新日历显示的日期
        cal = self._cal.monthdayscalendar(year, month)
        for indx, item in enumerate(self._items):
            week = cal[indx] if indx < len(cal) else []
            fmt_week = [('%02d' % day) if day else '' for day in week]
            self._calendar.item(item, values=fmt_week)

    def _show_select(self, text, bbox):
        x, y, width, height = bbox
        textw = self._font.measure(text)
        canvas = self._canvas
        canvas.configure(width=width, height=height)
        canvas.coords(canvas.text, (width - textw)/2, height / 2 - 1)
        canvas.itemconfigure(canvas.text, text=text)
        canvas.place(in_=self._calendar, x=x, y=y)

    def _pressed(self, evt=None, item=None, column=None, widget=None):
        """在日历的某个地方点击。"""
        if not item:
            x, y, widget = evt.x, evt.y, evt.widget
            item = widget.identify_row(y)
            column = widget.identify_column(x)
        if not column or not item in self._items:
            # 在工作日行中单击或仅在列外单击。
            return
        item_values = widget.item(item)['values']
        if not len(item_values):  # 这个月的行是空的。
            return
        text = item_values[int(column[1]) - 1]
        if not text:
            return
        bbox = widget.bbox(item, column)
        if not bbox:  # 日历尚不可见
            self.Cwindow.after(20, lambda: self._pressed(
                item=item, column=column, widget=widget))
            return
        text = '%02d' % text
        self._selection = (text, item, column)
        self._show_select(text, bbox)

    def _prev_month(self):
        """更新日历以显示前一个月。"""
        self._canvas.place_forget()
        self._selection = None
        self._date = self._date - mytimedelta(days=1)
        self._date = mydatetime(self._date.year, self._date.month, 1)
        self.CB_year.set(self._date.year)
        self.CB_month.set(self._date.month)
        self._update()

    def _next_month(self):
        """更新日历以显示下一个月。"""
        self._canvas.place_forget()
        self._selection = None
        year, month = self._date.year, self._date.month
        self._date = self._date + \
            mytimedelta(days=calendar.monthrange(year, month)[1] + 1)
        self._date = mydatetime(self._date.year, self._date.month, 1)
        self.CB_year.set(self._date.year)
        self.CB_month.set(self._date.month)
        self._update()

    def _update(self, event=None, key=None):
        """刷新界面"""
        if key and event.keysym != 'Return':
            return
        year = int(self.CB_year.get())
        month = int(self.CB_month.get())
        if year == 0 or year > 9999:
            return
        self._canvas.place_forget()
        self._date = mydatetime(year, month, 1)
        self._build_calendar()  # 重建日历
        if year == mydatetime.now().year and month == mydatetime.now().month:
            day = mydatetime.now().day
            for _item, day_list in enumerate(self._cal.monthdayscalendar(year, month)):
                if day in day_list:
                    item = 'I00' + str(_item + 2)
                    column = '#' + str(day_list.index(day)+1)
                    self.Cwindow.after(100, lambda: self._pressed(
                        item=item, column=column, widget=self._calendar))

    def _exit(self, confirm=False):
        if not confirm:
            self._selection = None
        self.Cwindow.destroy()

    def _main_judge(self):
        """判断窗口是否在最顶层"""
        try:
            if self.Cwindow.focus_displayof() == None or 'toplevel' not in str(self.Cwindow.focus_displayof()):
                self._exit()
            else:
                self.Cwindow.after(10, self._main_judge)
        except:
            self.Cwindow.after(10, self._main_judge)

    def selection(self):
        """返回表示当前选定日期的日期时间。"""
        if not self._selection:
            return None
        year, month = self._date.year, self._date.month
        return str(mydatetime(year, month, int(self._selection[0])))[:10]

    def Input_judgment(self, content):
        """输入判断"""
        if content.isdigit() or content == "":
            return True
        else:
            return False


class myTreeview(basicClass):
    """封装了Treeview, 方便使用在不同的窗口上, 但是继承basicClass默认是headings模式
    # 获取选择项需要进行event的绑定!

    Args:
        fatherWidget: 父控件,必须
        titles: treeview 标题,必须
        **kwargs: 主要是为了传递show参数,tree 显示树栏;headings显示列表栏;tree headings 表示显示所有栏
        # 注意:在tree模式下 第一列要为#0, 否则会有很多怪bug, tree模式还不行

    """

    def __init__(self, fatherWidget=None, titles=[('#1', '#2')], **kwargs):
        super().__init__()
        self.kwargs = kwargs
        self.treeview = ttk.Treeview(
            show=kwargs.get('show', 'headings'),
            master=fatherWidget,
            columns=[title[0] for title in titles]
        )

        #  设置表格文字居中
        for title in titles:
            self.treeview.column(title[0], anchor="center", width=title[1])
        for item in titles:
            self.treeview.heading(item[0], text=item[0])
        self.treeview.grid(row=kwargs.get('row', 0),
                           column=kwargs.get('column', 0),
                           columnspan=kwargs.get('columnspan', 3))
        self.bindEventDefault()  # 绑定一些事件, 主要是select事件
        self.returnData = []

    def bindEventDefault(self):  # 默认事件绑定
        def selectItem(event):
            print('----------')
            print('iid=', self.treeview.selection())  # 输入选中的行的iid值
            # 输出选中行的各参数值的键值对字典
            print(self.treeview.item(self.treeview.selection()))  # 这个是Dict类型
            # print('text=', self.treeview.item(
            #     self.treeview.selection(), option='text'))  # 输出某个参数的值
            print('value=', self.treeview.item(
                self.treeview.selection(), option='value'))  # 输出某个参数的值
            self.returnData = self.treeview.item(
                self.treeview.selection(), option='value')

        self.treeview.bind("<<TreeviewSelect>>", selectItem)  # 某行被选中事件

    def bindEven(self, eventName, func):
        """绑定Treeview的一些事件, 比如点击item, 快捷键等

        Args:
            eventName (str): 事件名称, 比如"<<TreeviewSelect>>"
            func (函数名): 事件处理回调函数, 会携带事件对象（Event）去调用 func 方法
        """

        # 事件, 比如  "<<TreeviewSelect>>"
        # eventName = "<<TreeviewSelect>>"
        self.classPrint(f'绑定了事件{eventName}到{func.__name__}')
        self.treeview.bind(eventName, func=func)
        # 事件处理
        pass

    def insertItem(self, values=('精品一房', '床、书桌、电脑'), treeNode=''):  # 插入一个item
        if self.kwargs.get('show', 'headings') == 'headings':
            self.treeview.insert('', END, values=values)
        pass

    def addTreeNode(self, treeNodeName='001'):
        """增加一个树栏, 树栏下可以有多个item, 主意item要在树栏对象下 还不能用

        Args:
            text (str, optional): 树栏标题. Defaults to '001'.
        """
        treeNode = self.treeview.insert('', END, text=treeNodeName, open=True)
        return treeNode

    def delAllItem(self):  # 删除所有的item, 主要是为了刷新用
        """删除treeview中所有的item
        """
        x = self.treeview.get_children()
        for item in x:
            self.treeview.delete(item)
        pass

    def getSelection(self) -> tuple:
        self.classPrint('选择treeview项')
        selection = self.treeview.item(
            self.treeview.selection(), option='value')
        return selection
    # 还不能这样用
    # def reInsertItem(self, values=('精品一房', '床、书桌、电脑')):  # 重新插入item
    #     self.delAllItem()
    #     self.insertItem(values=values)


class tk_Helper(basicClass):
    '''
    自己做的gui界面专用类，方便平时简单使用,类名统一用xxx_xxx的格式哦
    强烈要求！！！一定要写明指定参数名后在赋值
    '''

    def __init__(self, title='default title', **kwargs):
        '''
        :param title:str,窗口标题
        '''
        super().__init__()
        self.instanceName = 'tkinter界面助手:'
        if kwargs.get('mode') == 'toplevel':  # 有指定toplevel才会用toplevel模式
            self.classPrint('self.window 采用toplevel模式')
            self.window = tk.Toplevel()
        else:
            self.classPrint('self.window 采用root模式')  # 有写root 或者是没有写就是默认root模式
            self.window = tk.Tk()
        # self.window.geometry('680x400+100+100')
        self.window.title(title)
        self.basicStrVar = tk.StringVar()  # 定义一个基本StringVar，用于默认值
        self.basicStrVar.set("default")
        self.font = ('Arial', 12)  # 默认字体
        self.classPrint('版本号{}'.format(version))
        self.setIcon(r'../res/favicon.png')
        self.menuCount = 0  # 用于菜单界面的计数
        self.classPrint('初始化完成')
        self.window.protocol("WM_DELETE_WINDOW",
                             self.onclosing)  # 2022.03.29x新增的事件
        # 注册（绑定）窗口变动事件
        # self.window.bind('<Configure>', self.window_resize)

    def setIcon(self, path_iconFile):  # 设置窗口图标
        try:
            self.window.iconphoto(False, tk.PhotoImage(file=path_iconFile))
        except Exception:
            self.classPrint('设置窗口icon失败')

    # 显示窗口
    def show(self):
        '''
        最终要调用这个函数才能正确显示窗口
        '''
        self.window.mainloop()

    # 销毁窗口
    def quit(self):
        self.window.destroy()
        # destroy 比quit好用,quit会导致所有同类窗口都关闭

    # 关闭时候的执行动作
    def onclosing(self):
        print(self.instanceName, '窗口关闭')
        self.classPrint('宽度', self.window.winfo_width(),
                        '高度', self.window.winfo_height())

        self.window.destroy()

    def size(self, wx, wy):
        self.resize(wx, wy)

    # 重新定义窗口大小
    def resize(self, a, b, c=0, d=0):
        self.window.geometry(str(a)+'x'+str(b)+'+'+str(c)+'+'+str(d))
        self.window.update()

    def resizeFull(self):
        # 获取屏幕分辨率
        screenWidth = self.window.winfo_screenwidth()
        self.classPrint("screenWidth=", screenWidth)
        screenHeight = self.window.winfo_screenheight()
        self.classPrint("screenHeight=", screenHeight)
        self.window.geometry("%sx%s+%s+%s" % (screenWidth, screenHeight, 0, 0))

    # 作为基本cmd
    def basicCmd(self):
        self.classPrint(getNowTime()+' hello world')

    # Button 按钮控件方法
    def addButton(self, textVar=0, cmd=0, row=2, column=1, **kwargs):
        '''
        在界面上增加一个按钮,建议写明指定参数名后在赋值
        :param textVar:可以是str,也可以是tk.StringVar()
        :param cmd:函数指针，即按钮按下要执行的动作
        :param row:int,按钮的位置布局
        :param column:int,按钮的位置布局
        '''
        if not cmd:  # 没有赋值就默认basicCmd函数
            cmd = self.basicCmd
        if not textVar:
            textVar = self.basicStrVar
        if isinstance(textVar, type(tk.StringVar())):
            print("yes stringvar")
            botton1 = tk.Button(self.window,
                                textvariable=textVar,
                                font=self.font,
                                width=10,
                                height=1,
                                command=cmd)
        else:
            botton1 = tk.Button(self.window,
                                text=textVar,
                                font=self.font,
                                width=10,
                                height=1,
                                command=cmd)
        botton1.grid(row=row, column=column,
                     padx=kwargs.get('padx', 5),
                     pady=kwargs.get('pady', 5)
                     )  # 要指定参数名row和column才可以用哦,不然会报错
        return botton1

    # Button 按钮控件方法
    def addEntry(self, row, column, textvariable=None, state="normal", show=None, **kwargs):
        """在界面上增加一个单行文本输入框

        Args:
            row (int): 行号
            column (int): 列号
            textvariable (文本变量, optional): 可以是字符串也可以是tk的Var类型对象. Defaults to None.
            state (str, optional): 显示模式"normal" "disabled" 或 "readonly". Defaults to "normal".
            show (str, optional): 是否显示为密文形式=='*'. Defaults to None.
            columnspan (int, optional): 跨越的列号. Defaults to 1.
            width (int, optional): [description]. Defaults to 20.

        Returns:
            Entry: tk的Entry对象
        """
        # 1. Entry 组件可以设置的状态："normal"，"disabled" 或 "readonly"
        # （注意，它跟 "disabled" 相似，但它支持选中和拷贝，只是不能修改，而 "disabled" 是完全禁止）
        # 2. 默认值是 "normal"
        # 3. 注意，如果此选项设置为 "disabled" 或 "readonly"，那么调用 insert() 和 delete() 方法都会被忽略
        entry1 = tk.Entry(self.window,
                          textvariable=textvariable,
                          show=None,  # 显示成明文形式
                          font=self.font,
                          state=state,
                          width=kwargs.get('width', 20))
        entry1.xview('end')  # 显示到行的末尾
        entry1.grid(row=row, column=column,
                    columnspan=kwargs.get('columnspan', 1),
                    padx=kwargs.get('padx', 1),
                    pady=kwargs.get('pady', 5),
                    )
        return entry1

    def addText(self, row, column, width=80, height=16, **kwargs):
        """在界面上增加一个Text控件

        Args:
            row (int): 要放置的行
            column (int): 要放置的列
            width (int, optional): 控件宽度. Defaults to 80.
            height (int, optional): 控件高度. Defaults to 16.
            columnspan (int, optional): 要跨越的列数. Defaults to 3.

        Returns:
            Text: 返回一个Text对象
        """
        text1 = tk.Text(self.window, width=width, height=height)
        # columnspan 是横跨几个column的参数
        text1.grid(row=row, column=column,
                   columnspan=kwargs.get('columnspan', 3))
        return text1

    def addLabel(self, row, column, textVar):
        '''
        在界面中添加一个标签控件
        '''
        if isinstance(textVar, type(tk.StringVar())):
            label1 = tk.Label(self.window, textvariable=textVar)
        else:
            label1 = tk.Label(self.window, text=textVar)
        label1.grid(row=row, column=column)
        return label1

    def addMenu(self, menuTitle):
        '''
        在界面中增加一个菜单
        :param: menuTitle: 父菜单的标题，
        返回一个Menu对象，可以在Menu对象中add_command等操作
        '''
        # menu1 = tk.Menu(self.window,)
        # menu1.grid(row=row, column=column)
        # return menu1
        # 判断是否有加过一个menu，如果有就不用初始化Menu
        self.menuCount += 1
        print('self.menuCount', self.menuCount)
        if self.menuCount == 1:
            # 创建菜单栏
            self.MenuBar = tk.Menu(self.window)
            # 将菜单栏放到主窗口
            self.window.config(menu=self.MenuBar)
        # 创建文件菜单，不显示分窗
        fileBar = tk.Menu(self.MenuBar, tearoff=0)
        # 添加文件菜单项
        # fileBar.add_command(label=label1, command=cmd1)
        # fileBar.add_command(label="save")
        # fileBar.add_command(label="save as")
        # # 创建分割线
        # fileBar.add_separator()
        # fileBar.add_command(label="exit", command=self.window.destroy)
        # 将文件菜单添加到菜单栏
        self.MenuBar.add_cascade(label=menuTitle, menu=fileBar)
        # def deleteMenu():
        #     # 删除第一个位置菜单项
        #     fileBar.delete(0)
        # tk.Button(window, text="删除", command=deleteMenu).pack()
        return fileBar

    def addCheckButton(self, row, column, text, CheckVar, **kwargs):
        '''
        复选框控件
        '''
        checkButton1 = tk.Checkbutton(self.window,
                                      text=text,
                                      variable=CheckVar,
                                      onvalue=1,
                                      offvalue=0)
        checkButton1.grid(row=row, column=column)
        return checkButton1

    def addListBox(self, row, column, itemlist, **kwargs):
        '''
        列表框  #TODO
        :param row:int
        :param column:int
        :param itemlist:list

        '''
        listBox1 = tk.Listbox(self.window)
        for item in ["good", "nice", "handsome", "very good", "verynice"]:
            listBox1.insert(tk.END, item)
        listBox1.insert(tk.ACTIVE, "cool")
        listBox1.grid(row=row, column=column,
                      columnspan=kwargs.get('columnspan', 1))
        return listBox1

    def addTreeView(self, row, column, titles, columnspan=3):
        '''
        表格与树状标签
        :param row:int
        :param column:int
        :param titles:列表字典，列表[0]为标题名str，列表[1]为该列宽度像素int
        '''
        # 定义列的名称, columns就是列名列表
        treeView1 = ttk.Treeview(self.window,
                                 show="headings",
                                 columns=[title[0] for title in titles],
                                 selectmode=tk.EXTENDED
                                 )
        treeView1.grid(row=row, column=column, columnspan=columnspan)
        # # 设置表格文字居中
        for title in titles:
            treeView1.column(title[0], anchor="center", width=title[1])

        # treeView1.column("name", anchor="center")
        # treeView1.column("gender", anchor="center")
        # treeView1.column("age", anchor="center")
        # 设置表格头部标题
        # treeView1.heading('name', text='姓名')
        # treeView1.heading('gender', text='性别')
        # treeView1.heading('age', text='年纪')

        for item in titles:
            treeView1.heading(item[0], text=item[0])

        # 设置表格内容
        # lists = [
        #          {"name": "34", "gender": "男", "age": "58"},
        #          {"name": "yang", "gender": "男", "age": "18"},
        #          {"name": "郑", "gender": "女", "age": "25"}
        #          ]
        # for v in lists:
        #     # treeView1.insert('', END, values=(v.get("name"), v.get("gender"), v.get("age")))
        #     treeView1.insert('', END, values=[v.get(k) for k in columnsId])

            # # 获取当前点击行的值
            # def treeviewClick(event):  # 单击
            #     for item in treeView1.selection():
            #         item_text = treeView1.item(item, "values")
            #         print(item_text)

            # # 鼠标左键抬起
            # treeView1.bind('<ButtonRelease-1>', treeviewClick)

            # 鼠标选中一行回调，可以返回所有选中行, 这个函数可以复制到实例中做具体回调处理
            def selectTree(event):
                for item in treeView1.selection():
                    item_text = treeView1.item(item, "values")
                    print(item_text)
            # 选中行事件的绑定回调
            treeView1.bind('<<TreeviewSelect>>', selectTree)
        return treeView1

    def addToplevel(self, winWidth, winHeight, x, y):
        # 创建顶级窗口，未测试完成 TODO
        top_level = tk.Toplevel()
        top_level.title("新窗口")
        # top_level.lift()
        top_level.focus_get()
        # top_level.attributes("-topmost", True)  # 使窗口保持在所有其他窗口之上，请使用：
        top_level.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))
        tk.Label(top_level, text="i am yang").pack()

    def addDialogBox(self, title, message, boxType='askokcancel', initialvalue='10'):
        """弹出一个对话框, 对话框类型可以选择

        Args:
            title (str): 对话框标题
            message (str): 对话框内容
            boxType (str, optional): 对话框类型,
                有askokcancel, showerror, showwarning, askinteger, askstring.
                Defaults to 'askokcancel'.
            initialvalue (str, optional): 对话框初始值. Defaults to '10'.

        Returns:
            [type]: 根据对话框类型返回不同类型对象
        """
        '''
        tk中的弹出对话框,
        :param boxType: askokcancel 询问是or取消
        showerror 错误提示框
        '''
        # 注意要指定master值,这样才能
        # 返回值为True或者False,
        if boxType == 'askokcancel':
            dialogBox = tk.messagebox.askokcancel(master=self.window,
                                                  title=title,
                                                  message=message)
            self.classPrint(boxType, dialogBox)  # ok=True, cancel=False
            return dialogBox
        if boxType == 'showerror':
            dialogBox = tk.messagebox.showerror(master=self.window,
                                                title=title,
                                                message=message)
            self.classPrint(boxType, dialogBox)  # 返回值为：ok
            return dialogBox
        if boxType == 'showwarning':
            dialogBox = tk.messagebox.showwarning(master=self.window,
                                                  title=title,
                                                  message=message)
            self.classPrint(boxType, dialogBox)  # 返回值为：ok
            return dialogBox
        if boxType == 'askinteger':  # 获取整型（标题，提示，初始值）
            result1 = simpledialog.askinteger(
                title=title,
                prompt=message,
                initialvalue=initialvalue)
            self.classPrint(boxType, result1)
            return result1
        if boxType == 'askstring':  # 获取字符串
            result1 = simpledialog.askstring(
                title=title,
                prompt=message,
                initialvalue=initialvalue)
            self.classPrint(boxType, result1)
            return result1

    def addComboBox(self, row, column, optionValues, oneVar, **kwargs):
        '''
        添加下拉框,返回值为下拉框对象,采用 cbox.get()为获得当前值
        '''
        cBox = ttk.Combobox(self.window, textvariable=oneVar,
                            width=kwargs.get('width', 24))
        # 设置下拉数据
        cBox["value"] = optionValues
        # 设置默认的下拉框的值
        cBox.current(0)
        cBox.grid(row=row, column=column)
        return cBox

    def addSeparator(self, row, column, orient='horizontal'):
        ''' TODO
        添加分割符，Separator(父对象, orient=方向)
        '''
        seq1 = ttk.Separator(self.window, orient='horizontal')
        seq1.grid(row=row, column=column, sticky=tk.E+tk.W)
        return seq1

    def insertText(self, textWidget, insertStr=''):
        '''
        往text控件中插入文字
        :param textWidget:widget
        :param insertStr:str
        '''
        # textWidget.insert(INSERT, insertStr)
        textWidget.insert(END, insertStr)
        # 这个see就是确保index位置的内容可见
        if isinstance(textWidget, type(tk.Text)):
            textWidget.see(END)

    def insert2TreeView(self, treeViewWiget, insertData):
        '''
        插入数据到指定的TreeView控件中
        :param insertData:str
        '''
        treeViewWiget.insert('', 0, values=insertData)
        pass

    def delFromTreeView(self, treeViewWiget, item):
        '''
        删除数据从TreeView控件中
        建议在正文中使用这样的表达, 即从选择项中删除
        for item in tr1.selection():
            print('item tobedel ==', item)
            treeViewWiget.delete(item)
        '''
        treeViewWiget.delete(item)
        pass

    def clearTreeViewContent(self, treeViewWiget):
        '''
        清除数据从TreeView控件中

        '''
        x = treeViewWiget.get_children()
        for item in x:
            treeViewWiget.delete(item)

    def delTextContent(self, textWidget, ):
        textWidget.delete(0.0, END)

    def selectFile(self, which_stringvar):
        '''
        :param which_stringvar:要发送哪个变量到上述widget
        '''
        self.openFile(which_stringvar)
        # self.insertText(to_widget, which_stringvar.get())

    def openFile(self, variable: StringVar, fileDescription='Excel 文件', fileType='*.xlsx'):
        filename = askopenfile(mode='r', filetypes=[
            (fileDescription, fileType)])
        if filename is not None:
            self.classPrint('选择的文件名为{}'.format(filename.name))
            variable.set(filename.name)
            return variable
        else:
            self.classPrint('选择的文件为空，或者是未选择文件')
            return False

    def oneDialog(self):
        '''
        一个简单的对话框,用于用户输入一些简单的信息
        只能单独临时使用,不然可能产生mainloop冲突
        '''
        def clickOK():
            self.window.quit()
            # print(userInputVar.get())
        userInputVar = StringVar()
        # self.addDialogBox('用户输入', '请输入信息', 'askstring')
        # self.classPrint('试一下行不行')
        # self.show()
        # 密码输入，输入字符显示 * 符号
        self.window.geometry(str(300)+'x'+str(300))
        e1 = tk.Entry(self.window, textvariable=userInputVar, show='*')
        e1.pack()
        e1 = tk.Button(self.window, text='确定', command=clickOK)
        e1.pack()
        self.window.mainloop()
        # 关闭窗口,并获取用户输入
        return userInputVar.get()

    def TODO(self):
        # TODO
        # 设置窗口图标
        self.window.iconbitmap("./image/favicon.ico")

        # 设置窗口大小
        winWidth = 600
        winHeight = 400
        # 获取屏幕分辨率
        screenWidth = self.window.winfo_screenwidth()
        screenHeight = self.window.winfo_screenheight()

        x = int((screenWidth - winWidth) / 2)
        y = int((screenHeight - winHeight) / 2)

        # 设置主窗口标题
        self.window.title("TopLevel参数说明")
        # 设置窗口初始位置在屏幕居中
        self.window.geometry("%sx%s+%s+%s" % (winWidth, winHeight, x, y))

        # 设置窗口宽高固定
        self.window.resizable(0, 0)
        pass

    def disappear(self):
        '''用于将本窗口隐藏，配套appear()使用'''
        self.classPrint('将自身隐藏，但实际上还在运行')
        self.window.withdraw()

    def appear(self):
        '''用于将本窗口显示，配套disappear()使用'''
        self.classPrint('将自身显示')
        self.window.wm_deiconify()


class myToplevel(tk_Helper):
    # 封装toplevel，参考myTreeview 2022.04.12继承为tk_helper
    # 相当于在toplevel外面在封装一层，不是继承topleve类
    def __init__(self, fatherWidget=None, winWidth=100, winHeight=100):
        # super().__init__()  不继承父类的构造函数
        self.instanceName = 'Toplevel实例'
        self.debugSwitch = 1
        self.window = tk.Toplevel(master=fatherWidget)
        self.window.title('默认标题')
        self.window.attributes("-toolwindow", 1)  # 无最大化，最小化
        self.window.transient(master=fatherWidget)  # 窗口只置顶root之上
        # self.window.resizable(False, False)  # 不可调节窗体大小

        self.font = ('Arial', 12)  # 默认字体!~
        self.basicStrVar = StringVar()
        self.window.grab_set()  # 转化模式
        self.window.focus_force()  # 得到焦点
        self.window.update()  # 刷新后，下面代码才能得到正确的宽和高尺寸
        a, b = self.window.winfo_width(), self.window.winfo_height()  # 得到弹出窗体的宽和高
        # 左边距=主窗口左边距+[(主窗口宽－弹出窗体宽)/2]
        # c = fatherWidget.window.winfo_x()+((fatherWidget.window.winfo_width()-a)/2)
        c = 100
        # 上边距=主窗口上边距+[(主窗口高－弹出窗体高)/2]
        # d = fatherWidget.window.winfo_y()+((fatherWidget.window.winfo_height()-b)/2)
        d = 100
        self.window.geometry('%dx%d+%d+%d' %
                             (winWidth, winHeight, c, d))  # 弹出窗体相对主窗体居中显示
        self.backData = []  # 返回数据列表
        self.window.protocol(
            "WM_DELETE_WINDOW", self.onclosing)  # 2022.03.29x新增的事件
        self.setupUI()

    def setupUI(self):  # 继承后要修修
        self.window.focus_set()
        # self.window.wait_window()
        pass
        # self.addLabel(rowId, 0, textVar='注意：只要关闭本窗体，才可以操作其它窗体')

    # def getSelectData(self):
    #     self.classPrint('获取返回值')
    #     self.backData = self.treeView1.returnData
    #     return self.backData

    def onclosing(self):
        print('toplevel关闭')
        print(self.instanceName, '窗口关闭')
        self.classPrint('宽度', self.window.winfo_width(),
                        '高度', self.window.winfo_height())
        self.window.destroy()

    def hi(self):
        """测试用的
        """
        self.classPrint('hi 默认调试方法')


class myLableFrame(tk_Helper):
    """封装了labelFrame, 窗口对象为self.window, 注意, 有写在wiki中
    传递text='', row=1, column=1

    Args:
        text (str): 控件标题文字
        row (int): grid的行数
        column (int): grid的列数
    """    # 封装lableFrame，参考myTreeview

    def __init__(self, fatherWidget=None, **kwargs):
        self.instanceName = 'LabelFrame实例'
        self.debugSwitch = 1
        self.font = ('Arial', 12)  # 默认字体!~

        text = kwargs.get('text', 'Group1')
        bd = kwargs.get('bd', 3)
        self.window = tk.LabelFrame(
            master=fatherWidget, text=text, bd=bd, padx=8, pady=8)
        rowId = kwargs.get('row', 0)
        columnId = kwargs.get('column', 0)
        colspan = kwargs.get('columnspan', 4)
        sticky = kwargs.get('nw', None)
        # grid参数的padx 为x轴上的间隔, 可以查看wiki中的grid方法
        self.window.grid(row=rowId, column=columnId,
                         columnspan=colspan, padx=20, sticky=sticky)


if __name__ == "__main__":
    init_chdir()
    Jessica = tk_Helper('我是美猴王 真的那个 v1.0')
    Jessica.addButton(textVar='忽略1元内差额', row=2, column=2)
    # Jessica.addButton(textVar='连接网关', row=1, column=3)
    # Jessica.addButton(row=3, column=3)
    # Jessica.addButton(textVar='df', row=4, column=2)
    # Jessica.addEntry(show=None, row=1, column=2)
    # Jessica.addListBox(2, 1, ['111', '22'])
    titles = [("错误类型", 100), ("A表编号", 100), ("B表编号", 100),
              ("A表金额", 100), ("B表金额", 100)]
    lists = [
        {"name": "34", "gender": "男", "age": "58"},
        {"name": "yang", "gender": "男", "age": "18"},
        {"name": "郑", "gender": "女", "age": "25"}
    ]
    tr1 = Jessica.addTreeView(row=5, column=1, titles=titles)
    Jessica.insert2TreeView(
        tr1, ('金额错误', 'X12345R27', 'X12345R27', '4400', '5555'))
    Jessica.insert2TreeView(
        tr1, ('金额错误', 'X12345R23', 'X12345R24', '4430', '5555'))
    Jessica.insert2TreeView(
        tr1, ('金额错误', 'X12345R27', 'X12345R27', '2200', '5555'))
    Jessica.insert2TreeView(
        tr1, ('金额错误', 'X12345R29', 'X12345R29', '4400', '5555'))
    Jessica.resizeFull()
    Jessica.show()
