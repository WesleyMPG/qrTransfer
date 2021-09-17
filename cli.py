import argparse
import os, sys


parser = argparse.ArgumentParser(
    description='Provides a QRcode to download or upload a file. \
    Commands described here take server\'s poit of view. Have in \
    mind that '
)

parser.add_argument('-p',
                    metavar='path',
                    dest='path',
                    type=str,
                    help='- Path to the file wich download code \
                    will be generated. (Only -ptm mode)')

parser.add_argument('-ptm',
                    '--pc-to-mobile',
                    action='store_false',
                    help='- [DEFAULT] Start the program to upload \
                    a file to other device')

parser.add_argument('-mtp',
                    '--mobile-to-pc',
                    action='store_true',
                    help='- Start the program to download a file \
                    from another device'
)

args = parser.parse_args()

if not args.mobile_to_pc:
    if not args.path:
        print('Path (-p) not provided. Check help (-h) for more \
info.')
        sys.exit(1)

    if not os.path.isfile(args.path):
        print(f'The path {args.path} does not exist.')
        sys.exit(1)

    args.path = os.path.abspath(args.path)
else:
    args.pc_to_mobile = False

