import json
from string import Formatter
from typing import Optional, Type
from .schema import BaseModel

JSON_FORMAT_INSTRUCTIONS = {}
JSON_FORMAT_INSTRUCTIONS["en"] = """The output should be formatted as a JSON instance that conforms to the JSON schema below.

As an example, for the schema {{"properties": {{"foo": {{"title": "Foo", "description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}}
the object {correct_example} is a well-formatted instance of the schema. The object {wrong_example} is not well-formatted.

Here is the output schema:
```
{schema}
```"""

JSON_FORMAT_INSTRUCTIONS["zh"] = """输出内容应根据输出的schema格式化为JSON格式，具体格式参考以下案例。

例如输出的schema为 {{"properties": {{"foo": {{"title": "Foo", "description": "a list of strings", "type": "array", "items": {{"type": "string"}}}}}}, "required": ["foo"]}}
正确的输出应该为 {correct_example} . 而错误的输出为 {wrong_example}。

以下是输出的schema:
```
{schema}
```"""

class Templates(object):
    def __init__(self, 
                 prompt: str, 
                 field: Optional[Type[BaseModel]], 
                 language: str = "zh",
                 correct_example:str = None,
                 wrong_example:str = None):
        self.prompt = prompt
        self.field = field
        self.language = language

        if correct_example is not None:
            self.correct_example = correct_example
        else:
            self.correct_example = '{"foo": ["bar", "baz"]}'

        if wrong_example is not None:
            self.wrong_example = wrong_example
        else:
            self.wrong_example = '{"properties": {{"foo": ["bar", "baz"]}}}'

    def invoke(self, *args, **kwargs) -> str:
        schema = self.get_format_instructions()
        variables = self.get_template_variables()
        prompts = self.prompt
        for v in variables:
            prompts = prompts.replace(f"{{{v}}}", kwargs[v])
        prompts = prompts + "\n\n" + schema
        return prompts
    def get_format_instructions(self) -> str:
        schema = self.field.schema()
        
        reduced_schema = schema
        if "title" in reduced_schema:
            del reduced_schema["title"]
        if "type" in reduced_schema:
            del reduced_schema["type"]

        schema_str = json.dumps(reduced_schema, ensure_ascii=False)
        return JSON_FORMAT_INSTRUCTIONS[self.language].format(schema=schema_str, 
                                                              correct_example=self.correct_example, 
                                                              wrong_example=self.wrong_example)

    def get_template_variables(self):
        input_variables = {
            v for _, v, _, _ in Formatter().parse(self.prompt) if v is not None
        }

        return sorted(input_variables)
