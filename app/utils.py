from flask.json import JSONEncoder
from sqlalchemy_utils import Choice


# A custom JSON encoder for ChoiceType fields
class CustomJSONEncoder(JSONEncoder):
     def default(self, obj):
        if isinstance(obj, Choice):
            return obj.code

        return JSONEncoder.default(self, obj)
