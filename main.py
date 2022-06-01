import argparse
import os
from http.server import HTTPServer

import apprise

from server import MakeNotificationServer

parser = argparse.ArgumentParser(description='Simply send notifications to many sources')
parser.add_argument(
    '--to',
    metavar='url',
    type=str,
    default=os.getenv('NOTIFY_TO', default=None),
    help='The target notification service url. '
         '(More info: https://github.com/caronc/apprise). '
         '[env: NOTIFY_TO] (required)'
)
parser.add_argument(
    '--title',
    type=str,
    help='The message title'
)
parser.add_argument(
    '--attach',
    metavar='attach',
    type=str,
    nargs='+',
    help='Attach a file to the notification'
)
parser.add_argument(
    '--body',
    type=str,
    help='The message body'
)
parser.add_argument(
    '--listen',
    metavar='listen',
    type=int,
    help='Listen for http requests on specific port',
)

args = parser.parse_args()
if not args.to:
    exit(parser.print_help())

ap = apprise.Apprise()
ap.add(args.to)

if args.body:
    print("Sending...")
    ap.notify(
        title=args.title,
        body=args.body,
        attach=args.attach
    )
elif args.listen:
    serverPort = args.listen
    server = HTTPServer(('', serverPort), MakeNotificationServer(ap))

    print("Server started http://localhost:%s" % serverPort)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass

    server.server_close()
else:
    print("Either specify a body or provide the --listen parameter")
    exit(parser.print_help())

print("Done")
