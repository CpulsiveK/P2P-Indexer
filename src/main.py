import sys
sys.path.append('../')
from indexer.indexer import Indexer


def main():
    server = Indexer()
    server.startIndexer()


if __name__ == '__main__':
    main()