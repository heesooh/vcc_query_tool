import argparse


def get_arguments():
    parser = argparse.ArgumentParser(description='Process records between two dates.')
    parser.add_argument('-f', '--from-date', required=True, type=str, help='Start date in YYYY-MM-DD format')
    parser.add_argument('-t', '--to-date', required=True, type=str, help='End date in YYYY-MM-DD format')
    return parser.parse_args()