from argparse import ArgumentParser

def parse_arguments():
    parser = ArgumentParser()
    parser.add_argument("-i", "--input", help="Input file to read data")
    parser.add_argument("-o", "--output", help="Output data to write data.")
    parser.add_argument("-a", "--algorithm", help="Hashing algorithm to use; Available: MD5, SHA1, SHA256, SHA512", default="MD5")
    args = parser.parse_args()
    return args
