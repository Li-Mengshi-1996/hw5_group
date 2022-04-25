from mapping import *
import time


def main():
    start = time.time()
    active_measurement("71.192.200.239")
    end = time.time()

    print(end - start)


main()
