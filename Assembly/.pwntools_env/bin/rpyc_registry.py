#!/home/ahm4d_312/miniconda3/bin/python3.13
import sys
from rpyc.cli.rpyc_registry import main
if __name__ == '__main__':
    if sys.argv[0].endswith('.exe'):
        sys.argv[0] = sys.argv[0][:-4]
    sys.exit(main())
