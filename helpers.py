from flask import abort
from flask import Response as FlaskResponse
import json
import traceback


def load_body(request):
    """Parse and return request body or None on failure."""
    try:
        data = json.loads(request.data.decode())
    except json.decoder.JSONDecodeError as err:
        print("Error: %s\nStacktrace: %s" % (err, traceback.format_exc()))
        return None
    return data


class Response(FlaskResponse):
    """A custom JSON response."""

    def __init__(self, *args, **kwargs):
        response = kwargs.pop("response", "")
        return super(FlaskResponse, self).__init__(*args, response=json.dumps(response), content_type="application-json", **kwargs)
