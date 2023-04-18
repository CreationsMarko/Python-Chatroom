from argparse import ArgumentParser

def generate_args():
    parser = ArgumentParser(prog="Python Chatroom", description="End-to-End Encrypted Python Chatroom")

    parser.add_argument('-f', '--front', choices=['cli', 'gui'], default='cli')

    parser.add_argument('-a', '--address', default='127.0.0.1')
    parser.add_argument('-p', '--port', default='7077', type=int)
    parser.add_argument('-v', '--verbose', action='store_true')
    return parser.parse_args()