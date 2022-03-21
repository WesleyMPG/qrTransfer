import argparse, sys
from pathlib import Path

__all__ = ['args']


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
                    help='- [DEFAULT] Starts the program to upload \
                    a file to other device')

parser.add_argument('-mtp',
                    '--mobile-to-pc',
                    action='store_true',
                    help='- Starts the program to download a file \
                    from another device'
)

parser.add_argument('--remote',
                    action='store_true',
                    help='- Enables transfer through the remote \
                    service file.io'
)

parser.add_argument('--debug',
                    action='store_true',
                    help='- Enables debug mode.'
)


args = parser.parse_args()

if not args.mobile_to_pc:
    if not args.path_list:
        print('Path (-p) not provided. Check help (-h) for more \
info.')
        sys.exit(1)

    paths = args.path_list
    for i in range(len(paths)):
        paths[i] = Path(paths[i].strip()).absolute()
        p = Path(paths[i]).absolute()
        if not (paths[i].is_file() or paths[i].is_dir()):
            print(f'The path {paths[i]} does not exist.')
            sys.exit(1)

else:
    args.pc_to_mobile = False



if __name__ == '__main__':
    print(args.path_list)