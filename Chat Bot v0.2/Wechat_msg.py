import uiautomation as ui
import win32clipboard as w
import win32con
import threading
import time
from Openai_model import AI
class WeChat_Chat():
    def __init__(self,api_key,find_str = '@ChatGPT',temperature = 0,presence_penalty = 0,frequency_penalty = 0,max_tokens = 100,System = '',num_QA = 10):
        self.msg = ''#消息内容
        self.Replied_Messages = [None]#用于记录已回复的消息
        self.Got_Messages = [None]#用于记录已接收的消息
        self.temperature = temperature#用于控制ai回答的随机性0~1
        self.System = System
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.max_tokens = max_tokens
        self.num_QA = num_QA#ai最多储存的消息数量，用于控制ai的记忆
        self.Messages = list()#用于储存历史记录,这个历史记录要发给ai，这样才能使得ai能够联系上下文
        self.find_str = find_str#根据此字符串寻找对方的消息是否是需要用ai回答的
        self.running_flag = True#控制线程开始与停止
        self.ai = AI(api_key,self.temperature,self.presence_penalty,self.frequency_penalty,self.max_tokens,self.System)
        self.lock = threading.Lock()#创建锁对象
    #获取对方的消息
    def get_msg(self):
        while True:
            #try:
                #获取消息
                with self.lock:#关键操作锁一下防止出错
                    with ui.UIAutomationInitializerInThread():#多线程用uiautomation库的方法时必须加这个
                        msg_list = ui.ListControl(Name = '消息')
                        return_msg = msg_list.GetChildren()[-1].Name
                #找到最后一次@ChatGPT的内容
                return_msg_index = return_msg.rfind(self.find_str)
                if return_msg_index != -1:
                    return_msg = return_msg[return_msg_index:]#获取对方的消息
                    return_msg = return_msg.replace(self.find_str,'')#清除对方消息中的“@ChatGPT”字样
                    #确保不重复回复同样的消息
                    if return_msg not in self.Got_Messages:
                        #因为两个函数同时访问Got_Messages会产生冲突，所以有函数访问的时候要锁住,with代码块运行时自动获取锁，运行完毕自动释放锁
                        with self.lock:
                            self.Got_Messages.append(return_msg)
                            print('对方'+':'+return_msg)
                            print(self.Got_Messages)
                            #self.Messages['User:'+return_msg] = 0#做了一个处理，防止一开始没有历史消息导致ai发生错误
                            #return return_msg
                    else:
                        print('捕捉到重复消息！')
                        #return None
                else:
                    print('未捕捉到关键字！')
            #except:
                #print('Error')
        # 输出字符串位置
    def send_msg(self):
        while True:
            try:
                with self.lock:
                    reply_list = list(set(self.Got_Messages) - set(self.Replied_Messages))#获取一个需要回复的列表
                if len(reply_list) > 0:
                    #对待回复列表中的消息依次回复
                    for return_msg in reply_list:
                        self.Messages.append({"role": "user", "content": "{text}".format(text = return_msg)})
                        response =self.ai.Chat_AI(self.Messages)#获取AI的消息，此时可以让另一个函数运作
                        if 'AI:' in response['choices'][0]['message']['content']:
                            response['choices'][0]['message']['content'] = response['choices'][0]['message']['content'].replace('AI:','')#把ChatGPT回复的话里面的可能出现的“AI:”字样删除
                        if return_msg != None:
                            print('对于"{return_msg}"消息的自动回复:\n\n'.format(return_msg = return_msg) +response['choices'][0]['message']['content'])
                            self.msg = '对于"{return_msg}"消息的自动回复:\n\n'.format(return_msg = return_msg) + response['choices'][0]['message']['content']
                            self.Replied_Messages.append(return_msg)#将已回复的消息放进列表中
                            with open(file = 'WeChat_msg_data.txt',mode = 'a+',encoding='utf-8') as file:
                                file.write('User:'+return_msg+'\n')
                                file.write('AI:'+response['choices'][0]['message']['content']+'\n\n')
                            self.Messages.append({"role": "assistant", "content": "{response}".format(response = response['choices'][0]['message']['content'])})#将本次回复写入列表
                            #遗忘功能，防止ai储存的记忆过多导致错误，最多储存num_QA次QA
                            if len(self.Messages) >= self.num_QA:
                                self.Messages = self.Messages[2:]
                            #将测试消息放到剪贴板
                            w.OpenClipboard()
                            w.EmptyClipboard()
                            w.SetClipboardData(win32con.CF_UNICODETEXT,self.msg)
                            w.CloseClipboard()
                            with self.lock:
                                with ui.UIAutomationInitializerInThread():#多线程用uiautomation库的方法时必须加这个
                                    #发送消息，此方法会强制微信窗口置顶，不能完全实现后台输入
                                    wechat_window = ui.WindowControl(Name = '微信')
                                    wechat_window.SwitchToThisWindow(waitTime=0.5)
                                    if not wechat_window.IsTopmost():
                                        wechat_window.SetTopmost()#先将窗口置顶
                                    edit = ui.EditControl(Name = '输入')
                                    #time.sleep(0.5)#防止输入不全
                                    edit.SendKeys('{Ctrl}v',waitTime=0)
                                    edit.SendKeys('{Enter}',waitTime=0)
                else:
                    pass
            except:
                pass
    def running(self):
        try:
            #直接开两个线程让两个函数同时跑
            thread1 = threading.Thread(target=self.get_msg)
            thread2 = threading.Thread(target=self.send_msg)
            #开始两个线程
            thread1.start()
            thread2.start()
            #等待两个线程结束
            thread1.join()
            thread2.join()
        except:
            print('quite')