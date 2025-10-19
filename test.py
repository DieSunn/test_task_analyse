
import os
import pytest
from module import BrandRatingAnalyse

CSV_CONTENT = """name,brand,price,rating
iphone 15 pro,apple,999,4.9
galaxy s23 ultra,samsung,1199,4.8
redmi note 12,xiaomi,199,4.6
"""

def write_tmp_csv(tmp_path, name="data.csv", content=CSV_CONTENT):
    p = tmp_path / name
    p.write_text(content, encoding="utf-8")
    return str(p)

def test_read_csv_and_make_dict(tmp_path):
    f = write_tmp_csv(tmp_path)
    br = BrandRatingAnalyse([f], "average-rating")
    data = br.read_csv()
    assert isinstance(data, list)
    assert any(d["brand"] == "apple" for d in data)

    brands = br.make_dict(data)
    assert "apple" in brands
    assert brands["apple"] == [4.9]

def test_calculate_average_rating_multiple_rows(tmp_path):
    content = """name,brand,price,rating
            a,brand1,10,4.0
            b,brand1,20,2.0
            c,brand2,5,5.0
            """
    f = write_tmp_csv(tmp_path, "two.csv", content)
    br = BrandRatingAnalyse([f], "average-rating")
    data = br.read_csv()
    br.make_dict(data)
    avgs = br.calculate_average_rating()
    assert avgs["brand1"] == 3.0
    assert avgs["brand2"] == 5.0

def test_generate_report_output_contains_header_and_rows(tmp_path):
    f = write_tmp_csv(tmp_path)
    br = BrandRatingAnalyse([f], "average-rating")
    data = br.read_csv()
    br.make_dict(data)
    out = br.generate_report()
    # проверяем, что заголовок и бренд присутствуют в выводе
    assert "brand" in out
    assert "apple" in out
