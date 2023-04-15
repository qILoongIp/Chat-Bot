import openai
import asyncio
class AI():
    def __init__(self,api_key,temperature = 0):
        self.api_key = api_key
        self.temperature = temperature
        openai.api_key = self.api_key#通过密钥链接Openai
    def Chat_AI(self,return_msg,Messages = None):
        try:
            messages = [{
                        "role": "user", "content": "{text}".format(text = return_msg),#导入用户消息
                        "role": "assistant", "content": "{Used_Messages}".format(Used_Messages = Messages)#导入历史消息
                        }]
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages = messages, temperature=self.temperature, max_tokens=1000)
            return response
        except:
            return 'AI连接超时!'