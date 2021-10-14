import argparse
import os, sys


parser = argparse.ArgumentParser(
    description='Provides a QRcode to download or upload a file. \
    Commands described here take server\'s poit of view. Have in \
    mind that '
)

parser.add_argument('-p',
                    metavar='path_list',
                    dest='path_list',
                    nargs='+',
                    help='- Paths to the files wich download code \
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

parser.add_argument('--remote',
                    action='store_true',
                    help='- Enable transfer through the remote \
                    service file.io'
)

args = parser.parse_args()

if not args.mobile_to_pc:
    if not args.path_list:
        print('Path (-p) not provided. Check help (-h) for more \
info.')
        sys.exit(1)

    paths = args.path_list
    for i in range(len(paths)):
        paths[i] = os.path.abspath(paths[i])
        if not (os.path.isfile(paths[i]) or os.path.isdir(paths[i])):
            print(f'The path {paths[i]} does not exist.')
            sys.exit(1)

else:
    args.pc_to_mobile = False



if __name__ == '__main__':
    print(args.path_list)