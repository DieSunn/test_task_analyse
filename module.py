import csv
import os
from collections import defaultdict
from typing import DefaultDict, List, Dict, Any, Optional


class Report:
    """Базовый интерфейс отчёта."""
    def generate(self, data: DefaultDict[str, List[float]]) -> str:
        raise NotImplementedError


class AverageRatingReport(Report):
    def generate(self, data: DefaultDict[str, List[float]]) -> str:
        try:
            from tabulate import tabulate
        except Exception:
            # если tabulate не установлен, формируется простой табличный вывод
            rows = [("#", "brand", "average_rating")]
            sorted_items = sorted(
                ((b, (round(sum(r) / len(r), 2) if r else 0.0)) for b, r in data.items()),
                key=lambda x: (-x[1], x[0])
            )
            for idx, (brand, avg) in enumerate(sorted_items, start=1):
                rows.append((str(idx), brand, f"{avg:.2f}"))
            return "\n".join(f"{r[0]}\t{r[1]}\t{r[2]}" for r in rows)

        averages = []
        for brand, ratings in data.items():
            avg = round(sum(ratings) / len(ratings), 2) if ratings else 0.0
            averages.append((brand, avg))

        averages.sort(key=lambda x: (-x[1], x[0]))

        table_rows = [(idx, brand, avg) for idx, (brand, avg) in enumerate(averages, start=1)]
        table = tabulate(table_rows, headers=["#", "brand", "average_rating"], tablefmt="github", floatfmt=".2f")
        return table


class BrandRatingAnalyse:
    def __init__(self, filenames: List[str], report_name: Optional[str]) -> None:
        self.filenames = filenames or []
        self.report_name = report_name or "average-rating"
        self.brands: DefaultDict[str, List[float]] = defaultdict(list)
        self._reports: Dict[str, Report] = {
            "average-rating": AverageRatingReport()
        }

    def read_csv(self) -> List[Dict[str, Any]]:
        if not self.filenames:
            raise FileNotFoundError("No input files provided via --files")

        data: List[Dict[str, Any]] = []
        for filename in self.filenames:
            if not os.path.exists(filename):
                raise FileNotFoundError(f"File not found: {filename}")
            with open(filename, newline="", encoding="utf-8") as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    brand = (row.get("brand") or "").strip()
                    rating_str = (row.get("rating") or "").strip()
                    try:
                        rating = float(rating_str) if rating_str else 0.0
                    except ValueError:
                        rating = 0.0
                    data.append({"brand": brand, "rating": rating})
        return data

    def make_dict(self, data: List[Dict[str, Any]]) -> DefaultDict[str, List[float]]:
        self.brands = defaultdict(list)
        for entry in data:
            brand = entry.get("brand", "")
            rating = float(entry.get("rating") or 0.0)
            self.brands[brand].append(rating)
        return self.brands

    def calculate_average_rating(self) -> Dict[str, float]:
        averages: Dict[str, float] = {}
        for brand, ratings in self.brands.items():
            averages[brand] = self.average_sum(ratings)
        return averages

    def average_sum(self, nums: List[float]) -> float:
        if not nums:
            return 0.0
        return round(sum(nums) / len(nums), 2)

    def generate_report(self) -> str:
        report = self._reports.get(self.report_name)
        if not report:
            raise ValueError(f"Unknown report: {self.report_name}")
        output = report.generate(self.brands)
        print(output)
        return output


