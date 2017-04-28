#!/usr/bin/env python3.6

#  Built-in modules
from copy import deepcopy
from hashlib import md5, sha1, sha256, sha512
from os import path
from sys import exit, stderr
from gc import enable
from time import time

#  Internal modules
from args import parse_arguments
from database import t1  # Import SQLite3 table templates
from word import Word

#  External modules
from gevent.queue import Queue
from shemutils.logger import Logger
from shemutils.database import *
from shemutils.timer import Timer

log = Logger("Hash-Bank")
enable()  # Enable garbage collection
MAX_LINES = 1000000

class HashBank(object):
    """
    HashBank Object
    """
    def __init__(self, *args, **kwargs):
        args = args[0]
        self.queue = Queue()
        self.input_file = args.input
        self.input_fd = None
        self.output_file = args.output
        self.database_file = None
        self.algorithm = args.algorithm
        self.timer = Timer()
        self.start_time = time()
        self.computed = 0  # N Hashes computed by object
        self._start() # commence

    def _check_required(self):
        """
        Verify if required parameters are passed to the object
        """

        if not self.input_file or not self.output_file:
            log.critical("No input/output file specified.")
            exit(1)

        if path.exists(self.output_file):
            log.critical("File {0} already exists.".format(self.output_file))
            exit(1)

        # Create the database file
        self.database_file = Database(self.output_file)
        self._init_database()
        self.input_fd = open(self.input_file, "rb")
        return 0

    def _format_data(self, data):
        """
        Function to remove trailing newlines from lines.
        """
        if type(data) is not bytes:
            data = data.encode()

        return data.replace("\n".encode(), "".encode())

    def _read_data(self, max_val=MAX_LINES):
        """
        Function to extract data from an input file and insert it into the
        Queue to be processed later by the hashing object.

        Returns the number of lines rea`d from the file.
        """
        i = 0
        while i < max_val:
            line = self.input_fd.readline()
            if not line:
                return None
            line = self._format_data(line)
            self.queue.put_nowait(line)
            i += 1
        return i

    def _parse_algorithm(self, algorithm):
        """
        Parse the argument string to correspond into adequate hashing algorithm
        object supplied by hashlib
        """
        if algorithm == "MD5":
            return md5()
        elif algorithm == "SHA256":
            return sha256()
        elif algorithm == "SHA512":
            return sha512()
        elif algorithm == "SHA1":
            return sha1()
        else:
            log.critical("Unknown algorithm type {0}".format(algorithm))
            exit(1)

    def _hash_per_sec(self):
        if self.start_time:
            elapsed = time() - self.start_time
            return self.computed / elapsed

    def _report_insertion_status(self, iterator):
        if iterator % 5000 != 0:
            return None
        hsec = "%.2f" % self._hash_per_sec()
        stderr.write("Hashes computed: {0} | H/s: {1}\r".format(iterator, hsec))
        return 0

    def _hash_everything(self):
        i = 0
        while self.queue.empty() is False:
            to_hash = self.queue.get_nowait()
            w = Word(to_hash)
            for x in w.formats:
                algo = self._parse_algorithm(self.algorithm)
                algo.update(x)
                #print(algo.hexdigest())
                insert_query = t1.insert_data([x.decode(errors="ignore"), algo.hexdigest()])
                self.database_file.controller.execute(insert_query)
                del algo
                i += 1
                self.computed += 1
                self._report_insertion_status(i)

        self.database_file.save()
        log.info("Stored {0} hashes into HashBank {1}".format(i, self.output_file))
        return 0


    def _init_database(self):
        """
        Simply check the database object from shemutils module.
        """
        if not self.database_file:  # Check if database object is initialized
            log.critical("Database object is not initialized.")
            exit(1)

        queries_to_execute = [t1.create()]
        for query in queries_to_execute:
            self.database_file.controller.execute(query)
        return 0

    def _start(self):
        """
        Trigger function for object
        """
        self._check_required()  # check for required arguments.
        n_lines = self._read_data()
        log.info("Program have read {0} lines of data.".format(n_lines))
        if self.queue.empty() is True:  # check for emptiness
            log.critical("Queue is empty.")
            exit(1)
        while n_lines is not None:
            self._hash_everything()
            n_lines = self._read_data()
            log.info("Program have read {0} lines of data.".format(n_lines))


def main():
    args = parse_arguments()
    hObj = HashBank(args)
    log.info("Procedure took {0}".format(hObj.timer.stop_timer()))
    return 0


if __name__ == "__main__":
    main()
