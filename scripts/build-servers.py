import argparse
import shared

parser = argparse.ArgumentParser()
parser.add_argument('--dev', action='store_true')
parser.add_argument('--upload', action='store_true')
args = parser.parse_args()
if args.upload:
    shared.build_and_upload_servers()
else:
    shared.build_servers(args.dev)
