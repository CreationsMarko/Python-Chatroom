from ..client.cli import ClientCLI
from ..client.gui import ClientGUI
from ..common.args import generate_args


def main():
    args = generate_args()

    if args.front == 'cli':
        ClientCLI().connect(args.address, args.port)
    elif args.front == 'gui':
        ClientGUI().connect(args.address, args.port)


if __name__ == '__main__':
    main()