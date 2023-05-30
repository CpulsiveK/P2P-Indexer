from indexer import Indexer
from indexer_utils import unicastIndexerAddr

def main():
    indexerInstance = Indexer()
    indexerInstance.startIndexer()


if __name__ == '__main__':
    main()