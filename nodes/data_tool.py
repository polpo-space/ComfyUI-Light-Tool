import json
import re


class AnyType(str):
    def __ne__(self, __value: object) -> bool:
        return False


any_type = AnyType("*")


class KeyValue:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "data": ("STRING", {"default": '{"key": "This is value"}', "multiline": True}),
                "key": ("STRING", {"default": "key", "multiline": False})
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("value",)
    FUNCTION = "key_value"
    CATEGORY = 'ComfyUI-Light-Tool/DataProcessing'
    DESCRIPTION = "Get values from JSON string"

    @staticmethod
    def key_value(data, key):
        try:
            json_data = json.loads(data)
        except json.JSONDecodeError:
            return ''

        value = json_data
        parts = key.split('.')
        for part in parts:
            key_part = re.match(r'^([^\[]*)', part).group(1)
            indices = re.findall(r'\[(\d+)]', part)

            if key_part:
                if isinstance(value, dict):
                    value = value.get(key_part, '')
                else:
                    return ''
                if value == '':
                    return ''

            for index_str in indices:
                if isinstance(value, list):
                    try:
                        index = int(index_str)
                    except ValueError:
                        return ''
                    if 0 <= index < len(value):
                        value = value[index]
                    else:
                        return ''
                else:
                    return ''
        return (value if value != '' else '',)


class SerializeJsonObject:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_object": (any_type, {"default": json.loads('{"key": "This is value"}'), "defaultInput": True}),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("json_str",)
    FUNCTION = "get_json_str"
    CATEGORY = 'ComfyUI-Light-Tool/DataProcessing'
    DESCRIPTION = "Convert a JSON object to a JSON string"

    @staticmethod
    def get_json_str(json_object):
        try:
            json_str = json.dumps(json_object, ensure_ascii=False)
        except json.JSONDecodeError:
            return '{}'
        return (json_str,)


class DeserializeJsonString:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_str": ("STRING", {"default": '{"key": "This is value"}', "multiline": True}),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("json_object",)
    FUNCTION = "get_json"
    CATEGORY = 'ComfyUI-Light-Tool/DataProcessing'
    DESCRIPTION = "Convert a JSON string to a JSON object"

    @staticmethod
    def get_json(json_str):
        try:
            json_dict = json.loads(json_str)
            return (json_dict,)
        except json.JSONDecodeError:
            json_dict = {}
        return (json_dict,)


class DeserializeWownowProcessConfig:
    """
    Decode a Wownow process configuration JSON string into individual outputs.
    Upload targets are provider-neutral signed PUT URLs.
    """

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "json_str": (
                    "STRING",
                    {
                        "multiline": True,
                        "default": "",
                        "placeholder": (
                            '{\n'
                            '  "width": 1024,\n'
                            '  "height": 1024,\n'
                            '  "origin_image_url": "https://cdn.example.com/images/f3301718e9dbf7e7d703b73a144afa32.jpg",\n'
                            '  "uv_image_put_url": "https://storage.example.com/upload/uv.png?signature=...",\n'
                            '  "binary_image_put_url": "https://storage.example.com/upload/binary.png?signature=...",\n'
                            '  "depth_image_put_url": "https://storage.example.com/upload/depth.png?signature=...",\n'
                            '  "normalmap_image_put_url": "https://storage.example.com/upload/normal_map.png?signature=...",\n'
                            '  "outpaint_image_put_url": "https://storage.example.com/upload/outpaint.png?signature=..."\n'
                            '}'
                        ),
                    },
                )
            }
        }

    RETURN_TYPES = (
        "INT",
        "INT",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
        "STRING",
    )
    RETURN_NAMES = (
        "width",
        "height",
        "origin_image_url",
        "uv_image_put_url",
        "binary_image_put_url",
        "depth_image_put_url",
        "normalmap_image_put_url",
        "outpaint_image_put_url",
    )

    FUNCTION = "decode"
    CATEGORY = "ComfyUI-Light-Tool/DataProcessing"
    DESCRIPTION = (
        "Decode JSON into Wownow process settings and signed PUT upload URLs."
    )

    def _as_str(self, value, default=""):
        if value is None:
            return default
        return str(value)

    def _as_int(self, value, default=0):
        if value is None or value == "":
            return default
        try:
            return int(value)
        except Exception:
            return default

    def decode(self, json_str: str):
        data = {}
        if json_str and json_str.strip():
            try:
                data = json.loads(json_str)
                if not isinstance(data, dict):
                    data = {}
            except Exception:
                data = {}

        width = self._as_int(data.get("width", 0), default=0)
        height = self._as_int(data.get("height", 0), default=0)
        origin_image_url = self._as_str(data.get("origin_image_url", "")).strip()

        uv_image_put_url = self._as_str(data.get("uv_image_put_url", "")).strip()
        binary_image_put_url = self._as_str(data.get("binary_image_put_url", "")).strip()
        depth_image_put_url = self._as_str(data.get("depth_image_put_url", "")).strip()
        normalmap_image_put_url = self._as_str(
            data.get("normalmap_image_put_url", "")
        ).strip()
        outpaint_image_put_url = self._as_str(
            data.get("outpaint_image_put_url", "")
        ).strip()

        print(
            "[WownowProcessConfigDecoder] Parsed:",
            {
                "origin_image_url": origin_image_url,
                "width": width,
                "height": height,
                "uv_image_put_url": uv_image_put_url,
                "binary_image_put_url": binary_image_put_url,
                "depth_image_put_url": depth_image_put_url,
                "normalmap_image_put_url": normalmap_image_put_url,
                "outpaint_image_put_url": outpaint_image_put_url,
            },
        )

        return (
            width,
            height,
            origin_image_url,
            uv_image_put_url,
            binary_image_put_url,
            depth_image_put_url,
            normalmap_image_put_url,
            outpaint_image_put_url,
        )


class Calculate:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "number1": (any_type, {"defaultInput": False, "default": "1.0", "multiline": False}),
                "number2": (any_type, {"defaultInput": False, "default": "1.0", "multiline": False}),
                "operator": (any_type, {"defaultInput": False, "default": "+", "multiline": False}),
                "return_type": (["INT", "FLOAT", "STRING"], {"default": "FLOAT"}),
            },
            "optional": {
                "description": ("STRING", {"defaultInput": False, "default": "", "multiline": True}),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("result",)
    FUNCTION = "calculate"
    CATEGORY = 'ComfyUI-Light-Tool/DataProcessing'
    DESCRIPTION = "Simple numerical operations"

    @staticmethod
    def calculate(number1, number2, operator, return_type, description):

        def is_number(value):
            try:
                float(value)
                return True
            except ValueError:
                return False

        if not is_number(number1) or not is_number(number2):
            raise ValueError("Inputs 'a' and 'b' must be numbers or numeric strings.")

        number1 = float(number1)
        number2 = float(number2)

        if operator not in ['+', '-', '*', '/']:
            raise ValueError("Unsupported operator. Supported operators are '+', '-', '*', '/'.")

        if operator == '+':
            result = number1 + number2
        elif operator == '-':
            result = number1 - number2
        elif operator == '*':
            result = number1 * number2
        elif operator == '/':
            if number2 == 0:
                raise ZeroDivisionError("Division by zero is not allowed.")
            result = number1 / number2
        else:
            raise ValueError(f"Unsupported operator {operator}")

        if return_type == "FLOAT":
            result = float(result)
        elif return_type == "INT":
            result = round(result)
        else:
            result = str(result)
        return (result, )


class ConvertNumType:
    def __init__(self):
        pass

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "number": (any_type, {"default": '', "multiline": False}),
                "return_type": (["INT", "FLOAT", "STRING"], {"default": "INT"}),
            }
        }

    RETURN_TYPES = (any_type,)
    RETURN_NAMES = ("number",)
    FUNCTION = "convert"
    CATEGORY = 'ComfyUI-Light-Tool/DataProcessing'
    DESCRIPTION = "Convert numeric types"

    @staticmethod
    def convert(number, return_type):
        if return_type == "FLOAT":
            number = float(number)
        elif return_type == "INT":
            number = round(float(number))
        else:
            number = str(number)
        return (number,)



NODE_CLASS_MAPPINGS = {

    "Light-Tool: KeyValue": KeyValue,
    "Light-Tool: SerializeJsonObject": SerializeJsonObject,
    "Light-Tool: DeserializeJsonString": DeserializeJsonString,
    "Light-Tool: DeserializeWownowProcessConfig": DeserializeWownowProcessConfig,
    "Light-Tool: Calculate": Calculate,
    "Light-Tool: ConvertNumType": ConvertNumType,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Light-Tool: KeyValue": "Light-Tool: Get values from JSON",
    "Light-Tool: SerializeJsonObject": "Light-Tool: Serialize a JSON object",
    "Light-Tool: DeserializeJsonString": "Light-Tool: Deserialize a JSON string",
    "Light-Tool: DeserializeWownowProcessConfig": "Light-Tool: Wownow Process Config Decoder",
    "Light-Tool: Calculate": "Light-Tool: Calculate",
    "Light-Tool: ConvertNumType": "Light-Tool: Convert Num Type",
}
