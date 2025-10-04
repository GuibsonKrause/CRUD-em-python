from pathlib import Path

from crud_app.cli import run_cli


def main() -> None:
    data_file = Path(__file__).with_name("data.txt")
    run_cli(data_file)


if __name__ == "__main__":
    main()
