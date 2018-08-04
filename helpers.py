from flask import abort
import json
import traceback


def load_body(request):
    # parses and returns request body or return 400 on failure
    try:
        data = json.loads(request.data.decode())
    except json.decoder.JSONDecodeError as err:
        print("Error: %s\nStacktrace: %s" % (err, traceback.format_exc()))
        abort(400)
    return data
