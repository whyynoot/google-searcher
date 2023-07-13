from ac_searcher import AcSearcher
from config import config

def main():
    a = AcSearcher(config)
    a.run()

if __name__ == "__main__":
    main()