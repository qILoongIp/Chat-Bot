import openai
import asyncio
class AI():
    def __init__(self,api_key,temperature = 0,presence_penalty = 0,frequency_penalty = 0,max_tokens = 100,System = ''):
        self.api_key = api_key
        self.temperature = temperature
        self.presence_penalty = presence_penalty
        self.frequency_penalty = frequency_penalty
        self.max_tokens = max_tokens
        self.System = System
        openai.api_key = self.api_key#通过密钥链接Openai
    def Chat_AI(self,Messages = []):
        try:
            messages = [{"role": "system", "content": "{System}".format(System = self.System)}]
            messages.extend(Messages)
            response = openai.ChatCompletion.create(model="gpt-3.5-turbo",
                                                     messages = messages, #有问题
                                                     temperature=self.temperature, 
                                                     presence_penalty=self.presence_penalty,
                                                     frequency_penalty=self.frequency_penalty,
                                                     max_tokens=self.max_tokens)
            return response
        except:
            return 'AI连接超时!'