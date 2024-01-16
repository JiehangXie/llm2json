from json import JSONDecodeError, dumps
from .utils import parse_json_markdown

class JSONParser(object):
    """
    This function is a method of a class that takes a string as its input argument and aims to return a dictionary or JSON object. 
    It initially attempts to parse the input string into JSON format. If the parsing is successful, it returns the parsed dictionary. 
    However, if the parsing fails, it raises a ValueError exception, providing the reason for the JSON decoding error as part of the exception message.
    """

    def to_dict(self, text: str) -> dict:
        """Parse a LLM response to a Python dictionary.

            Args:
                text (str): The JSON string to be parsed.

            Returns:
                The parsed JSON object as a Python dictionary.
        """
        try:
            return parse_json_markdown(text)
        except JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")
        
    def to_json(self, text: str) -> str:
        """Parse a LLM response to a JSON Object.

            Args:
                text (str): The JSON string to be parsed.

            Returns:
                The parsed JSON object as a JSON Object.
        """
        try:
            result = parse_json_markdown(text)
            return dumps(result)
        except JSONDecodeError as e:
            raise ValueError(f"Invalid JSON string: {e}")

