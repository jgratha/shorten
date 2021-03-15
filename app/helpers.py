from datetime import datetime
from json import JSONEncoder


class CustomJSONEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m%dT%H:%M:%S.%f')[:-3] + 'Z'
        return JSONEncoder.default(self, obj)
