from env_manager import OUTPUT_FILE
from db_manager import session, Weather


def main() -> int:
    print(f"Hello! output: {OUTPUT_FILE}")

    return 0


if __name__ == "__main__":
    main()
