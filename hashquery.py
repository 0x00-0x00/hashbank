#!/usr/bin/env python3.6
from os import path
from sys import exit
from argparse import ArgumentParser
from shemutils.logger import Logger
from shemutils.database import *
from database import t1

log = Logger("HashQuery")


class HashQuery(object):
    def __init__(self, *args, **kwargs):
        self.args = args[0]

        if not self.args.file or not path.exists(self.args.file):
            log.critial("No database file to search for hashes or words.")
            exit(1)

        self.database_file = Database(self.args.file)

        if self.args.word is not None:
            search = t1.search("PLAIN_TEXT", self.args.word)
        elif self.args.hash is not None:
            search = t1.search("HASH", self.args.hash)
        else:
            log.critical("Neither hash nor word arguments had values.")
            exit(1)

        self.database_file.controller.execute(search)
        results = self.database_file.controller.get()
        for result in results:
            id, word, hash = result
            self._present_data((word, hash))


    @staticmethod
    def _present_data(data):
        print("Plain Text ....: %s\nHash ..........: %s\n\n" % (data[0], data[1]))
        return 0


def main():
    parser = ArgumentParser()
    parser.add_argument("-f", "--file", help="Database file to read data.", required=True)
    parser.add_argument("-w", "--word", help="Word to search for hashes.")
    parser.add_argument("-e", "--hash", help="Hash to search for words.")
    args = parser.parse_args()
    HashQuery(args)
    return 0


if __name__ == "__main__":
    main()
