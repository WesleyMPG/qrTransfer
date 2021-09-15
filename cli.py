import argparse
import os, sys


parser = argparse.ArgumentParser(
    description='Provides a QRcode to download a file'
)

parser.add_argument('Path',
                    metavar='path',
                    type=str,
                    help='The path to file')

args = parser.parse_args()

file_path = args.Path

if not os.path.isfile(file_path):
    print(f'The path {file_path} does not exist.')
    sys.exit(1)

file_path = os.path.abspath(file_path)
