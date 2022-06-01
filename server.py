import json
from cgi import parse_header, FieldStorage, parse_multipart
from http.server import BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

from apprise import Apprise

paramMappings = {
    "title": "title",
    "header": "title",
    "name": "title",

    "body": "body",
    "message": "body",
    "text": "body",
    "description": "body",
}


def assign_params(target: dict, source: dict):
    for key in paramMappings:
        if key in source:
            value = source[key]
            if isinstance(value, list):
                target[paramMappings[key]] = source[key][0]
            else:
                target[paramMappings[key]] = source[key]


def MakeNotificationServer(ap: Apprise):
    class NotificationServer(BaseHTTPRequestHandler):

        def do_GET(self):
            self.do()

        def do_POST(self):
            self.do()

        def do(self):
            request_url = urlparse(self.path)
            query = parse_qs(request_url.query)

            message = {}

            # Headers
            headers = {k.lower(): v for k, v in dict(self.headers).items()}
            assign_params(message, headers)

            # Query params
            assign_params(message, query)

            # Json Body
            content_type, pdict = parse_header(headers.get('content-type'))
            body = {}

            if content_type == 'application/json':
                length = int(headers.get('content-length'))
                body = json.loads(self.rfile.read(length))
                assign_params(message, body)
            elif content_type == 'application/x-www-form-urlencoded':
                fields = FieldStorage(
                    fp=self.rfile,
                    headers=self.headers,
                    environ={'REQUEST_METHOD': 'POST'}
                )
                for key in fields:
                    body[key.lower()] = fields.getvalue(key)
                assign_params(message, body)
            elif content_type == 'multipart/form-data':
                pdict['boundary'] = bytes(pdict['boundary'], 'utf-8')
                fields = parse_multipart(self.rfile, pdict)
                for key in fields:
                    value = fields.get(key)
                    if type(value) == list:
                        body[key.lower()] = value[0]
                    else:
                        body[key.lower()] = value
                assign_params(message, body)

            print(json.dumps(
                {
                    "headers": headers,
                    "query": query,
                    "body": body,
                    "result": message,
                },
                indent=2
            ))

            attach = (
                message.get('attach')
            )
            # ap.notify(
            #     body=message.get('body'),
            #     title=message.get('title'),
            #     attach=attach,
            # )

            self.send_response(200)
            self.end_headers()

    return NotificationServer
