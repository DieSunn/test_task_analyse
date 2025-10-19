import argparse
import sys
from module import BrandRatingAnalyse

def main(argv=None):
    parser = argparse.ArgumentParser(description="test")
    parser.add_argument(
        '--files',
        nargs='+',
        help="Список входных файлов"
    )
    parser.add_argument(
        "--report",
        help="Имя выходного файла"
    )

    args = parser.parse_args(argv)

    try:
        br = BrandRatingAnalyse(args.files, args.report)
        data = br.read_csv()
        br.make_dict(data)
        br.generate_report()
    except Exception as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())