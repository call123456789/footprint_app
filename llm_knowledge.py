import openai
import json

class LLM_knowledge:
    def __init__(self, temperature=0.3, task="你是个出题能手"):
        self.temperature = temperature
        self.task = task
        self.messages = [{"role": "system", "content": task}]

        with open('API.json', 'r') as file:
            config = json.load(file)

        self.model = config.get('talk-model')
        self.api = config.get('api_key')
        self.base_url = config.get('base_url')

        self.client = openai.OpenAI(api_key=self.api, base_url=self.base_url)

    def add(self, content, role="user"):
        self.messages.append({"role": role, "content": content})

    def response(self, context="None"):
        if context != "None":
            self.messages.append({"role": "user", "content": context})
        try:
            completion = self.client.chat.completions.create(
                model=self.model,
                messages=self.messages,
                temperature=self.temperature
            )
            response_text = completion.choices[0].message.content
            self.messages.append(completion.choices[0].message)
            try:
                response_data = json.loads(response_text)
                # 确保返回的数据包含所需的键
                if "question" in response_data and "options" in response_data and "correct_answer" in response_data:
                    return response_data
                else:
                    return {"error": "返回的数据格式不正确"}
            except json.JSONDecodeError:
                # 如果解析失败，返回一个默认的 JSON 对象
                return {"error": "无法解析返回的内容为 JSON 格式"}
        except Exception as e:
            print(f"发生错误：{e}")
            return {"error": str(e)}