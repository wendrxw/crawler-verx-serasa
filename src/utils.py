import argparse


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--region",
        type=str,
        help="Filtrar por região (Argentina, Brasil, etc)."
    )

    return parser.parse_args()