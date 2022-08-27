import json


class Json:
    @staticmethod
    def parse_from_json(content):
        try:
            return json.loads(content)
        except:
            return None

    @staticmethod
    def parse_to_json(content):
        try:
            return json.dumps(content)
        except:
            return None
    