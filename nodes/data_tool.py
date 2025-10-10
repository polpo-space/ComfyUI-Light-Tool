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


# SaveURLsToHistory：聚合多个 URL 并作为最终输出显示在历史中
class SaveURLsToHistory:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                # 至少一个输入口可接上游节点输出
                "file_url_1": ("STRING", {"defaultInput": True, "default": ""}),
            },
            "optional": {
                # 可再接更多（需要更多就按此格式继续加）
                "file_url_2": ("STRING", {"defaultInput": True, "default": ""}),
                "file_url_3": ("STRING", {"defaultInput": True, "default": ""}),
                "file_url_4": ("STRING", {"defaultInput": True, "default": ""}),                
                # 输出为 JSON（建议 true，方便 API 解析）
                "return_json": ("BOOLEAN", {"default": True}),
            }
        }

    OUTPUT_NODE = True                  # 作为最终节点
    RETURN_TYPES = ("STRING",)          # 返回一个字符串（JSON或拼接）
    RETURN_NAMES = ("urls",)
    FUNCTION = "save"
    CATEGORY = "ComfyUI-Light-Tool/History"
    DESCRIPTION = "聚合多个URL并写入历史"

    def _parse_extra(self, s):
        s = (s or "").strip()
        if not s:
            return []
        # 先尝试按 JSON 数组解析
        try:
            data = json.loads(s)
            if isinstance(data, list):
                return [str(x).strip() for x in data if str(x).strip()]
        except Exception:
            pass
        # 退化为按换行或逗号分割
        parts = [p.strip() for p in s.replace("\r", "").replace(",", "\n").split("\n")]
        return [p for p in parts if p]

    def save(self,
             file_url_1="",
             file_url_2="",
             file_url_3="",
             file_url_4="",             
             return_json=True):

        urls = []
        for u in [file_url_1, file_url_2, file_url_3, file_url_4]:
            u = (u or "").strip()
            if u:
                urls.append(u)    
        # 去重并保序
        seen = set()
        deduped = []
        for u in urls:
            if u not in seen:
                seen.add(u)
                deduped.append(u)

        # 历史可见的 UI 文本（每个 URL 一行）
        ui = {"ui": {"text": deduped if deduped else ["<no urls>"]}}

        # 返回字符串：JSON 或换行拼接
        out = json.dumps(deduped) if return_json else ("\n".join(deduped))
        return (out,), ui


NODE_CLASS_MAPPINGS = {

    "Light-Tool: KeyValue": KeyValue,
    "Light-Tool: SerializeJsonObject": SerializeJsonObject,
    "Light-Tool: DeserializeJsonString": DeserializeJsonString,
    "Light-Tool: Calculate": Calculate,
    "Light-Tool: ConvertNumType": ConvertNumType,
    "Light-Tool: SaveURLsToHistory": SaveURLsToHistory
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "Light-Tool: KeyValue": "Light-Tool: Get values from JSON",
    "Light-Tool: SerializeJsonObject": "Light-Tool: Serialize a JSON object",
    "Light-Tool: DeserializeJsonString": "Light-Tool: Deserialize a JSON string",
    "Light-Tool: Calculate": "Light-Tool: Calculate",
    "Light-Tool: ConvertNumType": "Light-Tool: Convert Num Type",
    "Light-Tool: SaveURLsToHistory": "Light-Tool: Save URLs to History (Final)"
}
