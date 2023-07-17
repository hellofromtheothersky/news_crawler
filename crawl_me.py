import argparse
from website.Crawler import *


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--s', type=str, help="website name")
    parser.add_argument('--nc', type=int, default=-1, help="number of cate")
    parser.add_argument('--nn', type=int, default=-1, help="number of news per cate")

    args = parser.parse_args()
    name=args.s
    if name=='kenh14':
        c=Kenh14Crawler(name)
    elif name=='thanhnien':
        c=ThanhnienCrawler(name)
    elif name=='vtv':
        c=VtvCrawler(name)

    c.process(args.nc, args.nn, from_zero=False)
    