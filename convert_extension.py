import os
import argparse

def main():
    parser = argparse.ArgumentParser(
        description='This script support converting extension format img to txt')
    parser.add_argument('--input', type=str, default=None,
                        help='path to input directory.')
    parser.add_argument('--output', type=str, default=None,
                        help='path to output directory.')

    args = parser.parse_args()
    input = args.input
    output = args.output
    for r, d, f in os.walk(input):
        a = [os.path.join(r,os.path.splitext(i)[0]) for i in f]
        b = [i+'.txt' for i in a]
        c = [os.path.split(i)[1] for i in b]
        d = [os.path.join(output, i) for i in c]
        os.makedirs(output, exist_ok=True)
        for i in d:
            e = open(i, 'w')
            e.close()

if __name__ == '__main__':
    main()

