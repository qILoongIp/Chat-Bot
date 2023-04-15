from QQ_msg import QQ_Chat
from Wechat_msg import WeChat_Chat
class Main():
    def __init__(self,api_key = None,QQ_username = None,find_str = '@ChatGPT',temperature = 0):
        self.api_key = api_key
        self.QQ_username = QQ_username
        self.find_str = find_str
        self.temperature = temperature
        self.qq_chat = QQ_Chat(api_key = self.api_key,name = QQ_username,find_str = self.find_str,temperature = self.temperature)
        self.wechat_chat = WeChat_Chat(api_key = self.api_key,find_str = self.find_str,temperature = self.temperature)
        
    #对接QQ
    def main_for_QQ(self):
        self.qq_chat.running_flag = True
        self.qq_chat.running()
    def stop_main_for_QQ(self):
        self.qq_chat.running_flag = False

    #对接WeChat
    def main_for_WeChat(self):
        self.wechat_chat.running_flag = True
        self.wechat_chat.running()
    def stop_main_for_WeChat(self):
        self.wechat_chat.running_flag = False
if __name__ == '__main__':
    api_key = ''
    find_str = '@ChatGPT'#根据此字符串寻找对方的消息是否是需要用ai回答的
    choose = 2 #选择接入qq还是微信，qq是1，微信是2
    temperature = 0
    if choose == 1:
        QQ_username = '少龙'
        main = Main(api_key = api_key,QQ_username = QQ_username,find_str = find_str,temperature = temperature)
        main.main_for_QQ()
    elif choose == 2:
        main = Main(api_key = api_key,find_str = find_str,temperature = temperature)
        main.main_for_WeChat()