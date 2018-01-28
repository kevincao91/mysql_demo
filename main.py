from tkinter import *
import sys
import douban_remarks_download as douban

root = Tk()  # 创建窗口 初始化Tk()
root.title("豆瓣电影影评信息分析")  # 设置窗口标题
root.geometry("700x100")  # 设置窗口大小 注意：是x 不是*
root.resizable(width=False, height=False)  # 设置窗口是否可以变化长/宽，False不可变，True可变，默认为True

frame_1 = Frame(root)
lable_1 = Label(frame_1, text="网址：")
lable_1.pack(padx=20, pady=10, side=LEFT)
text_string = Variable()
entry_entity = Entry(frame_1, textvariable=text_string, width=80)
entry_entity.pack(padx=20, pady=5, side=RIGHT)
text_string.set("请输入你需要采集的豆瓣电影网址：")  # 设置文本框中的值
frame_1.pack(side=TOP)

frame_2 = Frame(root)
button_entity_1 = Button(frame_2, text="开始", command=lambda: douban.main(entry_entity.get()))
button_entity_1.pack(padx=20, pady=10, side=LEFT)
button_entity_2 = Button(frame_2, text="退出", command=sys.exit)
button_entity_2.pack(padx=20, pady=10, side=RIGHT)
frame_2.pack()

root.mainloop()  # 进入消息循环
