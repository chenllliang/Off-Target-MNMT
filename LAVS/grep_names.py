# 提取目录下所有文件的后缀名
# Usage: python grep_names.py [dir]

import os
import sys

def get_suffixes(dir):
    suffixes = set()
    for root, dirs, files in os.walk(dir):
        for file in files:
            suffix = os.path.splitext(file)[-1].replace(".", "")
            suffixes.add(suffix)
    return suffixes

if __name__ == "__main__":
    dir = sys.argv[1]
    suffixes = get_suffixes(dir)
    print(suffixes)
    print(len(suffixes))
