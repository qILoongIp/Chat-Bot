import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from main import Main
import threading
import sys
class UI:
    def __init__(self, master):
        self.master = master
        master.title("Chat Bot")
        
        # 创建三个选项卡
        self.tabControl = ttk.Notebook(master)
        self.tab1 = ttk.Frame(self.tabControl)
        self.tab2 = ttk.Frame(self.tabControl)
        self.tab3 = ttk.Frame(self.tabControl)
        self.tabControl.add(self.tab1, text='QQ bot')
        self.tabControl.add(self.tab2, text='WeChat bot')
        self.tabControl.add(self.tab3, text='注意事项')
        self.tabControl.pack(expand=1, fill="both")

        # 创建QQ bot选项卡中的UI元素
        self.name_label = tk.Label(self.tab1, text="聊天窗体名字")
        self.name_label.grid(row=0, column=0, padx=5, pady=5)
        self.name_entry = tk.Entry(self.tab1)
        self.name_entry.grid(row=0, column=1, padx=5, pady=5)
        self.api_label = tk.Label(self.tab1, text="Api_key")
        self.api_label.grid(row=1, column=0, padx=5, pady=5)
        self.api_entry = tk.Entry(self.tab1)
        self.api_entry.grid(row=1, column=1, padx=5, pady=5)
        self.find_label = tk.Label(self.tab1, text="查找关键字")
        self.find_label.grid(row=2, column=0, padx=5, pady=5)
        self.find_entry = tk.Entry(self.tab1)
        self.find_entry.insert(0, "@ChatGPT")  # 设置默认值
        self.find_entry.grid(row=2, column=1, padx=5, pady=5)
        self.System_label = tk.Label(self.tab1, text="System")
        self.System_label.grid(row=3, column=0, padx=5, pady=5)
        self.System_entry = tk.Entry(self.tab1)
        self.System_entry.insert(0, "一个有用的助手")  # 设置默认值
        self.System_entry.grid(row=3, column=1, padx=5, pady=5)
        self.temperature_label = tk.Label(self.tab1, text="Temperature")
        self.temperature_label.grid(row=4, column=0, padx=5, pady=5)
        self.temperature_slider = tk.Scale(self.tab1, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, length=200)
        self.presence_penalty_label = tk.Label(self.tab1, text="presence_penalty")
        self.presence_penalty_label.grid(row=5, column=0, padx=5, pady=5)
        self.presence_penalty_slider = tk.Scale(self.tab1, from_=-2, to=2, resolution=0.1, orient=tk.HORIZONTAL, length=200)
        self.frequency_penalty_label = tk.Label(self.tab1, text="frequency_penalty")
        self.frequency_penalty_label.grid(row=6, column=0, padx=5, pady=5)
        self.frequency_penalty_slider = tk.Scale(self.tab1, from_=-2, to=2, resolution=0.1, orient=tk.HORIZONTAL, length=200)
        self.max_tokens_label = tk.Label(self.tab1, text="max_tokens")
        self.max_tokens_label.grid(row=7, column=0, padx=5, pady=5)
        self.max_tokens_slider = tk.Scale(self.tab1, from_=0, to=2048, resolution=1, orient=tk.HORIZONTAL, length=200)
        self.num_QA_label = tk.Label(self.tab1, text="AI最大记忆消息数")
        self.num_QA_label.grid(row=8, column=0, padx=5, pady=5)
        self.num_QA_slider = tk.Scale(self.tab1, from_=10, to=100, resolution=1, orient=tk.HORIZONTAL, length=200)
        self.temperature_slider.set(0)  # 设置默认值
        self.temperature_slider.grid(row=4, column=1, padx=5, pady=5)
        self.presence_penalty_slider.set(0)  # 设置默认值
        self.presence_penalty_slider.grid(row=5, column=1, padx=5, pady=5)
        self.frequency_penalty_slider.set(0)  # 设置默认值
        self.frequency_penalty_slider.grid(row=6, column=1, padx=5, pady=5)
        self.max_tokens_slider.set(100)  # 设置默认值
        self.max_tokens_slider.grid(row=7, column=1, padx=5, pady=5)
        self.num_QA_slider.set(10)  # 设置默认值
        self.num_QA_slider.grid(row=8, column=1, padx=5, pady=5)
        self.start_button = tk.Button(self.tab1, text="开始", command=self.start_qq_bot)
        self.start_button.grid(row=9, column=0, padx=5, pady=5, sticky='w')
        self.start_button.bind('<Control-F1>', self.start_qq_bot)  # 设置快捷键
        self.stop_button = tk.Button(self.tab1, text="停止", command=self.stop_qq_bot)
        self.stop_button.grid(row=9, column=1, padx=5, pady=5, sticky='e')
        self.stop_button.bind('<Control-F2>', self.stop_qq_bot)  # 设置快捷键
        # 创建WeChat bot选项卡中的UI元素
        self.api_label2 = tk.Label(self.tab2, text="Api_key")
        self.api_label2.grid(row=0, column=0, padx=5, pady=5)
        self.api_entry2 = tk.Entry(self.tab2)
        self.api_entry2.grid(row=0, column=1, padx=5, pady=5)
        self.find_label2 = tk.Label(self.tab2, text="查找关键字")
        self.find_label2.grid(row=1, column=0, padx=5, pady=5)
        self.find_entry2 = tk.Entry(self.tab2)
        self.find_entry2.insert(0, "@ChatGPT")  # 设置默认值
        self.find_entry2.grid(row=1, column=1, padx=5, pady=5)
        self.System_label2 = tk.Label(self.tab2, text="System")
        self.System_label2.grid(row=2, column=0, padx=5, pady=5)
        self.System_entry2 = tk.Entry(self.tab2)
        self.System_entry2.insert(0, "一个有用的助手")  # 设置默认值
        self.System_entry2.grid(row=2, column=1, padx=5, pady=5)
        self.temperature_label2 = tk.Label(self.tab2, text="Temperature")
        self.temperature_label2.grid(row=3, column=0, padx=5, pady=5)
        self.temperature_slider2 = tk.Scale(self.tab2, from_=0, to=2, resolution=0.1, orient=tk.HORIZONTAL, length=200, showvalue=True)
        self.presence_penalty_label2 = tk.Label(self.tab2, text="presence_penalty")
        self.presence_penalty_label2.grid(row=4, column=0, padx=5, pady=5)
        self.presence_penalty_slider2 = tk.Scale(self.tab2, from_=-2, to=2, resolution=0.1, orient=tk.HORIZONTAL, length=200)
        self.frequency_penalty_label2 = tk.Label(self.tab2, text="frequency_penalty")
        self.frequency_penalty_label2.grid(row=5, column=0, padx=5, pady=5)
        self.frequency_penalty_slider2 = tk.Scale(self.tab2, from_=-2, to=2, resolution=0.1, orient=tk.HORIZONTAL, length=200)
        self.max_tokens_label2 = tk.Label(self.tab2, text="max_tokens")
        self.max_tokens_label2.grid(row=6, column=0, padx=5, pady=5)
        self.max_tokens_slider2 = tk.Scale(self.tab2, from_=0, to=2048, resolution=1, orient=tk.HORIZONTAL, length=200)
        self.num_QA_label2 = tk.Label(self.tab2, text="AI最大记忆消息数")
        self.num_QA_label2.grid(row=7, column=0, padx=5, pady=5)
        self.num_QA_slider2 = tk.Scale(self.tab2, from_=10, to=100, resolution=1, orient=tk.HORIZONTAL, length=200)
        self.temperature_slider2.set(0)  # 设置默认值
        self.temperature_slider2.grid(row=3, column=1, padx=5, pady=5)
        self.presence_penalty_slider2.set(0)  # 设置默认值
        self.presence_penalty_slider2.grid(row=4, column=1, padx=5, pady=5)
        self.frequency_penalty_slider2.set(0)  # 设置默认值
        self.frequency_penalty_slider2.grid(row=5, column=1, padx=5, pady=5)
        self.max_tokens_slider2.set(100)  # 设置默认值
        self.max_tokens_slider2.grid(row=6, column=1, padx=5, pady=5)
        self.num_QA_slider2.set(10)  # 设置默认值
        self.num_QA_slider2.grid(row=7, column=1, padx=5, pady=5)
        self.start_button2 = tk.Button(self.tab2, text="开始", command=self.start_wechat_bot)
        self.start_button2.grid(row=8, column=0, padx=5, pady=5, sticky='w')
        self.start_button2.bind('<Control-F1>', self.start_wechat_bot)  # 设置快捷键
        self.stop_button2 = tk.Button(self.tab2, text="停止", command=self.stop_wechat_bot)
        self.stop_button2.grid(row=8, column=1, padx=5, pady=5, sticky='e')
        self.stop_button2.bind('<Control-F2>', self.stop_wechat_bot)  # 设置快捷键
        
        # 创建注意事项选项卡中的UI元素
        self.note_label = tk.Label(self.tab3, text="请注意以下事项：")
        self.note_label.pack(pady=10)
        self.note1_label = tk.Label(self.tab3, text="1. 本程序使用前请将聊天窗口打开并置顶。")
        self.note1_label.pack(anchor='w', padx=20)
        self.note2_label = tk.Label(self.tab3, text="2. 本程序运行期间尽量不要操纵鼠标，否则有可能导致程序错误。")
        self.note2_label.pack(anchor='w', padx=20)
        self.note3_label = tk.Label(self.tab3, text="3. 本程序须在科学上网的前提下使用。")
        self.note3_label.pack(anchor='w', padx=20)
        self.note4_label = tk.Label(self.tab3, text="4. Api_key为OpenAI官方给出的Api_key。")
        self.note4_label.pack(anchor='w', padx=20)
        self.note5_label = tk.Label(self.tab3, text="5. 程序运行时屏幕上最好不要有其他窗口。")
        self.note5_label.pack(anchor='w', padx=20)
        self.note6_label = tk.Label(self.tab3, text="6. temperature:该参数用于控制生成的文本随机性的程度。")
        self.note6_label.pack(anchor='w', padx=20)
        self.note7_label = tk.Label(self.tab3, text="7. presence_penalty:该参数用于控制模型是否会重复之前已经生成的文本。")
        self.note7_label.pack(anchor='w', padx=20)
        self.note8_label = tk.Label(self.tab3, text="8. frequency_penalty:该参数用于控制模型是否会重复之前已经生成的文本。")
        self.note8_label.pack(anchor='w', padx=20)
        self.note9_label = tk.Label(self.tab3, text="9. max_tokens:该参数用于控制生成的文本的最大长度（以 token 为单位）。")
        self.note9_label.pack(anchor='w', padx=20)
        self.note10_label = tk.Label(self.tab3, text="10. System:此参数有助于设置助手的行为。")
        self.note10_label.pack(anchor='w', padx=20)


    # 开始QQ bot
    def start_qq_bot(self, event=None):
        # 检查输入是否为空
        if self.name_entry.get() == "" or self.api_entry.get() == "" or self.find_entry.get() == "":
            messagebox.showwarning("警告", "所有字段都必须填写！")
            return
        
        name = self.name_entry.get()
        api_key = self.api_entry.get()
        find_str = self.find_entry.get()
        temperature = self.temperature_slider.get()
        presence_penalty = self.presence_penalty_slider.get()
        frequency_penalty = self.frequency_penalty_slider.get()
        max_tokens = self.max_tokens_slider.get()
        System = self.System_entry.get()
        num_QA = self.num_QA_slider.get()
        main = Main( api_key, name,find_str, temperature,presence_penalty,frequency_penalty,max_tokens,System,num_QA)
        #main.main_for_QQ()
        # 创建新线程来启动主程序
        self.t1 = threading.Thread(target=main.main_for_QQ, args=())
        self.t1.setDaemon(True)  # 设置为守护线程，可以在主线程结束时自动退出
        self.t1.start()
        
    # 停止QQ bot
    def stop_qq_bot(self, event=None):
        '''main = Main()
        main.stop_main_for_QQ()'''
        sys.exit()

    # 开始WeChat bot
    def start_wechat_bot(self, event=None):
        # 检查输入是否为空
        if self.api_entry2.get() == "" or self.find_entry2.get() == "":
            messagebox.showwarning("警告", "所有字段都必须填写！")
            return

        api_key = self.api_entry2.get()
        find_str = self.find_entry2.get()
        temperature = self.temperature_slider2.get()
        presence_penalty = self.presence_penalty_slider2.get()
        frequency_penalty = self.frequency_penalty_slider2.get()
        max_tokens = self.max_tokens_slider2.get()
        System = self.System_entry2.get()
        num_QA = self.num_QA_slider2.get()
        main = Main(api_key = api_key,find_str = find_str,temperature = temperature,presence_penalty = presence_penalty,frequency_penalty = frequency_penalty,max_tokens = max_tokens,System = System,num_QA = num_QA)
        #main.main_for_WeChat()
        self.t2 = threading.Thread(target=main.main_for_WeChat, args=())
        self.t2.setDaemon(True)  # 设置为守护线程，可以在主线程结束时自动退出
        self.t2.start()

    # 停止WeChat bot
    def stop_wechat_bot(self, event=None):
        '''Main().stop_main_for_WeChat()'''
        sys.exit()


if __name__ == '__main__':
    root = tk.Tk()
    ui = UI(root)
    root.mainloop()