import argparse, sys, __main__
from pathlib import Path

__all__ = ['args']


def setup_arg_parser():
    parser = argparse.ArgumentParser(
        description='Provides a QrCode to download or upload a file. \
        Commands described here take server\'s point of view. Have that \
        in mind '
    )

    parser.add_argument('-p',
                        metavar='path_list',
                        dest='path_list',
                        nargs='+',
                        help='- Paths to the files which download code \
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
                        dest='shall_remote_upload',
                        help='- Enables transfer through the remote \
                        service file.io'
    )

    parser.add_argument('--debug',
                        action='store_true',
                        help='- Enables debug mode.'
    )
    return parser.parse_args()


def validate_args(args):
    if  args.mobile_to_pc:
        args.pc_to_mobile = False
    else:
        validate_path_list(args)


def validate_path_list(args):
    if not args.path_list:
        print('Path (-p) not provided. Check help (-h) for more info.')
        sys.exit(1)

    paths = args.path_list
    for i, path_str in enumerate(paths):
        paths[i] = Path(path_str.strip()).absolute()
        validate_path(paths[i])


def validate_path(p : Path):
    if (p.is_file() or p.is_dir()): return True
    print(f'The path {p} does not exist.')
    sys.exit(1)


class MockArgs:
    mobile_to_pc = True
    pc_to_mobile = False
    debug = False


name_of_main_file = Path(__main__.__file__).name
if not 'pytest' in sys.modules and name_of_main_file == 'main.py':
    args = setup_arg_parser() 
    validate_args(args)
else:
    args = MockArgs()



if __name__ == '__main__':
    print(args.path_list)