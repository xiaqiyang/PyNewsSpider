import tkinter as tk
from tkinter import ttk
import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

window = tk.Tk()
window.title('新闻热点爬虫')
window.geometry('400x300')

var1 = tk.StringVar()                    #网站
var2 = tk.StringVar()                    #关键词
new_websites = ["新浪", "新华", "凤凰"]
keywords = ["体育", "娱乐", "家居", "房产", "教育", "时尚", "时政", "游戏", "科技", "财经"]

#画布背景
canvas = tk.Canvas(window, width=400, height=300)
image_file = tk.PhotoImage(file='spider.png')
image = canvas.create_image(200, 150, anchor='center', image=image_file)
canvas.pack(side='top')

#标题
tk.Label(window, text='新闻热点爬虫程序', font=('Arial', 10), bg='white').place(x=155, y=35)


#可选下拉框
tk.Label(window, text='新闻网站:', bg='white').place(x=75, y=75)
tk.Label(window, text='新闻主题:', bg='white').place(x=75, y=95)

ttk.Combobox(window, values=new_websites, textvariable=var1).place(x=135, y=75)
ttk.Combobox(window, values=keywords, textvariable=var2).place(x=135, y=95)


# 新闻展示窗口
def news_display():
    if var1.get() and var2.get():
        news_window = tk.Toplevel(window)
        news_window.geometry('700x500')
        news_window.title('新闻展示')

#打开数据库
        if var1.get() == "新浪":
            mydb = myclient["SinaNews"]
        elif var1.get() == "新华":
            mydb = myclient["XinhuaNews"]
        elif var1.get() == "凤凰":
            mydb = myclient["FengHuangNews"]

        mycol = mydb[var2.get()]


        var = tk.StringVar()
        l1 = tk.Label(news_window, textvariable=var, bg='green', fg='white', font=('Arial', 12), width=30,
                      height=2).pack()
        var.set(var1.get() + '-' + var2.get())

        t = tk.Text(news_window, font=('Arial', 12), width=400, height=300)


#{}, {"_id": 0, "title": 1, "content": 1}

        num = 0
        for x in mycol.find():
            num = num+1
            t.insert("insert", str(num) + ". ")
            t.insert("insert", x.setdefault('title', ' ') + '\n    ' + x.setdefault('publish_time', ' ') + '\n    ' + x.setdefault('content_url', ' ') + '\n')

        t.pack()


#开始爬虫按钮
tk.Button(window, text="开始", bg='white', width='8', command=news_display).place(x=177, y=125)
window.mainloop()