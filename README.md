# test_task_analyse

Cкрипт для формирования отчёта average-rating по CSV файлам.

Запуск:
1) Установите зависимость для красивого вывода (опционально):
   pip install tabulate pytest

2) Пример:
   python main.py --files samples/a.csv samples/b.csv --report average-rating

Тесты:
   pip install -U pytest
   pytest -q

Как добавить новый отчёт:
 - Наследовать Report и реализовать метод generate(self, data).
 - Зарегистрировать в BrandRatingAnalyse._reports с ключом (имя отчёта).
