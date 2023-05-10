from ..server import Server
from ..common.args import generate_args

def main():
    args = generate_args()

    server = Server()
    print('Server Started! \n')
    server.start(args.address, args.port)

if __name__ == '__main__':
    main()