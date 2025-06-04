from  llm import LLM
from openai import OpenAI
import json
from painter import Painter

class tool_LLM(LLM):
    def __init__(self,temprature=0.3,InitInfo=""):
        super().__init__(temprature=temprature, task=sys_prompt)
        self.tools = tools
        self.now_response = {}
        self.painter = Painter()
        self.add(InitInfo)
    def response(self, context = "None"):
        # 记忆功能，通过不断往self.messages里面append信息实现
        if context != "None":
            self.messages.append({"role": "user", "content": context})
        self.now_response = {}
        while True:
            client = OpenAI(
                api_key=self.api,
                base_url=self.base_url,
            )
            completion = client.chat.completions.create(
                model = self.model,
                messages = self.messages,
                temperature = self.temprature,
                tools = self.tools
            )
            #得到回复
            new_message = completion.choices[0]
            self.messages.append(new_message.message)
            if new_message.message.tool_calls == None:
                break

            for tool_call in new_message.message.tool_calls:
                args = json.loads(tool_call.function.arguments)
                self.now_response[tool_call.function.name] = list(args.values())[0]
                self.messages.append({"role":"tool","tool_call_id": tool_call.id,"content": '已完成'})
            
        self.painter.response(self.now_response['painter'], 'resources/icon/travel.png')
        return self.now_response
    

#所有可调用的工具在这里，解释在每个工具的代码里面有写
tools =[
    {
        "type":"function",
        "function":{
            "name": "time",  #这是工具名字
            "description":"更新当前时间，每次都要调用", #这是工具的作用
            "parameters":{    #这是该工具的参数信息
                "type":"object",
                "properties": {   
                    "new_time":{
                        "type":"string",
                        "description":"更新后的时间，包括日期和几点钟"
                    }
                },
                "required": ["new_time"]
            }
        },
        "strict": True
    },
    {
        "type":"function",
        "function":{
            "name": "scene",  #这是工具名字
            "description":"更新场景描述", #这是工具的作用
            "parameters":{    #这是该工具的参数信息
                "type":"object",
                "properties": {   
                    "new_scene":{
                        "type":"string",
                        "description":"更新后的场景的描述"
                    }
                },
                "required": ["new_scene"]
            }
        },
        "strict": True
    },
    {
        "type":"function",
        "function":{
            "name": "event",  #这是工具名字
            "description":"更新发生的事件", #这是工具的作用
            "parameters":{    #这是该工具的参数信息
                "type":"object",
                "properties": {   
                    "new_event":{
                        "type":"string",
                        "description":"更新后的发生的事件"
                    }
                },
                "required": ["new_event"]
            }
        },
        "strict": True
    },
    {
        "type":"function",
        "function":{
            "name": "choice",  #这是工具名字
            "description":"更新下一次行动可能的选择", #这是工具的作用
            "parameters":{    #这是该工具的参数信息
                "type":"object",
                "properties": {   
                    "choices":{
                        "type":"list",
                        "description":"下一次动作可行的选择，注意是一个列表，元素个数控制在1-4个"
                    }
                },
                "required": ["choices"]
            }
        },
        "strict": True
    },
    {
        "type":"function",
        "function":{
            "name": "painter",  #这是工具名字
            "description":"画一幅场景画", #这是工具的作用
            "parameters":{    #这是该工具的参数信息
                "type":"object",
                "properties": {   
                    "prompt":{
                        "type":"string",
                        "description":"画的内容的说明，要说明风格是摄影照"
                    }
                },
                "required": ["prompt"]
            }
        },
        "strict": True
    }
]

sys_prompt = '''
你是一个模拟旅行软件里面的助手，用户会输入他想干的事情
你的任务是调用工具完成以下工作：
1.调用time工具更新用户完成了某件事时的时间，时间的表述尽可能简短
2.调用scene工具更新用户做旅行中所看到的场景
3.调用event工具更新用户会遇上的突发事件
4.调用choice工具更新用户下一步可能做出的选择，注意这个选择性调用，当下一步的动作比较确定时，比如遇上了下雨，选择出去还是不出去这种类似情况才选择调用
5.调用painter工具绘制用户所见的场景
注意：
所有的输出都不要出现敏感词
随后你会收到用户旅行的时间段、一起旅行的人和旅行地点。
如果旅行时间到达给定的时间，请提示用户旅行已结束，并给出返程交通方式，不要输出其他任何信息
如果用户是与特定身份的人一起旅行，如父母或爱人，请在event工具中以随机概率更新与这些特定身份有关的事件，比如与女朋友就选择哪些景点发生争吵或是互相体贴照顾的表现。
所有的场景和事件都必须与用户选择的旅行目的地相关，譬如当地的特色景区、特色美食
结合时间和地点判断旅行时的气候和可能的活动，譬如去北方的海边游泳不能在冬天
请快速做出回复，不用想太多
'''