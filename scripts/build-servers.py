import argparse

import shared


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dev', action='store_true')
    args = parser.parse_args()
    shared.build_servers(args.dev)


main()
