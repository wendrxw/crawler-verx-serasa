from src.driver import Handler
from src.utils import parse_args
from src.logger import setup_logger


def main():
    args = parse_args()

    handler = Handler(args.region)
    results = handler.run()
    handler.load_as_csv(results)

    return results


if __name__ == "__main__":
    main()
