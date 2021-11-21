import os
import sys

def minus_one():
    all_file = os.listdir(data_dir)
    for f in all_file:
        if f.endswith('txt'):
            file = open(data_dir+f, 'r')
            info = file.readlines()
            out_file = open(out_dir+f, 'w')
            for line in info:
                if line.strip() == '':
                    continue
                new_line = str(int(line[0]) - 1) + line[1:]
                out_file.write(new_line)
            file.close()
            out_file.close()


def to_zero():
    all_file = os.listdir(data_dir)
    for f in all_file:
        if f.endswith('txt'):
            file = open(data_dir + f, 'r')
            info = file.readlines()
            out_file = open(out_dir + f, 'w')
            for line in info:
                if line.strip() == '':
                    continue
                new_line = '0' + line[1:]
                out_file.write(new_line)
            file.close()
            out_file.close()


if __name__ == '__main__':
    data_dir = '~Desktop/data/train/labels'
    cmd = sys.argv[1]
    out_dir = sys.argv[2]

    if cmd == '0':
        to_zero()
    elif cmd == '1':
        minus_one()
