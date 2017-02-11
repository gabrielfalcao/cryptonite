import argparse

parser = argparse.ArgumentParser(
    prog='cryptonite import',
    description='imports a key')

parser.add_argument('key', metavar='<key>', help='as string, with linebreaks')
