from src.driver import Handler


def main():
    handler = Handler()
    results = handler.run()
    handler.load_as_csv(results)
    return results


if __name__ == "__main__":
    main()
