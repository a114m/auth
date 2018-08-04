from flask import abort
import json


def load_body(request):
    # parses and returns request body or return 400 on failure
    try:
        data = json.loads(request.data.decode())
    except json.decoder.JSONDecodeError:
        abort(400)
    return data
