import sys
sys.path.append('../')
from indexer.indexer import Indexer


def main():
    server = Indexer()
    server.startServer()


if __name__ == '__main__':
    main()