<center><img src="./assets/logo.png" /></center>
<p />
⚡LLM2Json⚡是一个易于使用的格式化大语言模型输出工具包，它的主要设计思想和部分实现代码参考 <a href="https://github.com/langchain-ai/langchain">LangChain</a>（但输出效果初步测试优于Langchain）。它可以通过自动构建prompts引导大语言模型输出符合JSON语法的返回数据，解决了大语言模型格式化输出、数据交互、前端开发等遇到的数据格式相关问题，使下游的应用程序、GPTs、Agents等开发更加方便快捷。

# 🚀快速开始
> 在线Notebook运行：https://aistudio.baidu.com/projectdetail/7412328?contributionType=1
## pip 安装

```bash
pip install llm2json
```

## 第一个 Hello World

### 1. 构造返回数据结构体

```python
from llm2json.prompts.schema import BaseModel, Field

class Xiaohongshu(BaseModel):
    title: str = Field(description="文章标题")
    context: str = Field(description = "正文内容")
    keywords: list = Field(description = "关键词")
```

### 2.  给定返回数据正确案例
> （可选项，但建议配置）

```python
correct_example = '{"title":"文章标题", "context":"正文内容", "keywords":["关键词1","关键词2"]}'
```

### 3. 生成模板

```python
from llm2json.prompts import Templates

t = Templates(prompt="""
              请你为商品：<{topic}>写一篇小红书文案。
              包括文章标题、正文内容和关键词，同时正文需要包含emoji表情
              """, 
          field=Xiaohongshu,
          correct_example=correct_example)

template = t.invoke(topic="文心牌润唇膏")
```

### 4. 格式化返回结果

> [!NOTE]
> 
> ernieChat() 是基于文心ErnieBot SDK封装的LLM内容生成函数，可替换成任意LLMs接口输入。
> 
> 具体实现可参考：[GitHub - PaddlePaddle/ERNIE-SDK: ERNIE Bot Agent is a Large Language Model (LLM) Agent Framework, powered by the advanced capabilities of ERNIE Bot and the platform resources of Baidu AI Studio.](https://github.com/PaddlePaddle/ERNIE-SDK)

```python
from llm2json.output import JSONParser

ernieResult = ernieChat(template)
parser = JSONParser()
print(parser.to_dict(ernieResult))
```

### 5. 生成效果

```json
{
    'title': '文心牌润唇膏，滋润保湿不粘腻！',
    'context': '✨想要拥有水润双唇吗？试试文心牌润唇膏！💦质地轻盈，一抹即化，保湿效果超赞！💋',
    'keywords': ['文心牌润唇膏', '保湿', '轻盈质地', '水润双唇']
}
```

# 📚演示案例

1. 情感分类
   
   ```python
   class Senta(BaseModel):
       sentiment: str = Field(description="情感倾向，取值为positive或negative")
   
   t = Templates(prompt="""
                 我会给你一段评论，请你判断这段评论是正面还是负面的。
                 评论内容是：{sentiment}
                 """, 
                 field=Senta,
             )
   
   template = t.invoke(sentiment="蛋糕味道不错，店家服务也很热情")
   
   ernieResult = ernieChat(template)
   parser = JSONParser()
   print(parser.to_dict(ernieResult))
   ```
   
   ```json
   {'sentiment': 'positive'}
   ```

2. 地址提取
   
   ```python
   class Address(BaseModel):
       city: str = Field(description="地级市")
   
   t = Templates(prompt="""
                 我会给你一个地址，请你从中提取出地级市名称。
                 地址是：{address}
                 """, 
                 field=Address,
             )
   
   template = t.invoke(address="湖北省武汉市汉阳区琴台大道附近")
   
   ernieResult = ernieChat(template)
   parser = JSONParser()
   print(parser.to_dict(ernieResult))
   ```
   
   ```json
   {'city': '武汉市'}
   ```

3. 生成模拟数据
   
   ```python
   class Data(BaseModel):
       name: str = Field(description="姓名")
       idcode: str = Field(description="18位数的身份证号")
       sex: str = Field(description="性别")
       phone: str = Field(description="手机号")
       email: str = Field(description="邮箱")
       address: str = Field(description="居住地址")
       date: str = Field(description="入职日期")
   
   t = Templates(prompt="""
                 请你根据模板生成入职人员测试数据
                 """, 
             field=Data,
             )
   
   template = t.invoke()
   
   ernieResult = ernieChat(template)
   parser = JSONParser()
   print(parser.to_dict(ernieResult))
   ```
   
   ```json
   {
       'name': '张三',
       'idcode': '123456789012345678',
       'sex': '男',
       'phone': '13800138000',
       'email': 'zhangsan@example.com',
       'address': '北京市朝阳区建国门外大街甲8号',
       'date': '2021-11-21'
   }
   ```

4. More examples will be comming soon…
