import apprise
import argparse
import os

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
    'body',
    type=str,
    help='The message body'
)

args = parser.parse_args()
if not args.to:
    exit(parser.print_help())

# Either specify message to send or http port to listen on
if not args.body:
    exit(parser.print_help())

ap = apprise.Apprise()
ap.add(args.to)

if args.body:
    ap.notify(
        title=args.title,
        body=args.body,
        attach=args.attach
    )

