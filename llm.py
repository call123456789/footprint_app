from openai import OpenAI
import json
#大语言模型类，其他很多代码需要使用到
class LLM:
    #默认使用通义千问大模型
    def __init__(self, temprature = 0.3, task = "你是个好助手"):
        self.temprature = temprature
        self.task = task
        self.messages = [ {"role": "system", "content": task} ]

        # 加载 JSON 文件
        with open('API.json', 'r') as file:
            config = json.load(file)

        # 获取 API 密钥
        self.model = config.get('model')
        self.api = config.get('api_key')
        self.base_url = config.get('base_url')
    def add(self, content, role = "user"):
        self.messages.append({"role": role, "content": content})
    def response(self, context = "None"):
        # 记忆功能，通过不断往self.messages里面append信息实现
        if context != "None":
            self.messages.append({"role": "user", "content": context})
        try:
            client = OpenAI(
                api_key=self.api,
                base_url=self.base_url,
            )
            completion = client.chat.completions.create(
                model = self.model,
                messages = self.messages,
                temperature = self.temprature
            )
            #得到回复
            self.messages.append(completion.choices[0].message)
            return completion.choices[0].message.content
        except:
            print("请检查您在API.json中填写的信息是否正确")
            return ' '
    
if __name__=='__main__':
    llm = LLM()
    print(llm.response('你好'))