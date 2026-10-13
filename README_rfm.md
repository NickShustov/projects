# RFM-сегментация клубов топ-5 лиг по трансферной активности

Анализ трансферного рынка: клубы топ-5 европейских лиг рассматриваются как «покупатели» и делятся на сегменты методом RFM (Recency, Frequency, Monetary). Период: сезоны 2015/16 – 2025/26.

## Данные
[transfermarkt-datasets](https://github.com/dcaribou/transfermarkt-datasets) — файл `transfermarkt-datasets.duckdb` (таблицы `transfers` и `clubs`). Файл в репозиторий не включён из-за размера, скачайте его по ссылке:
https://drive.google.com/drive/my-drive?dmr=1&ec=wgc-drive-%5Bmodule%5D-goto 

## Что сделано
- очистка данных: возвраты из аренды, молодёжные команды, неполные данные за 2026 год
- расчёт RFM по клубам (Recency считается по крупным сделкам сезона)
- 6 сегментов с учётом среднего чека
- анализ по лигам, чистые траты (покупки и продажи), стиль торговли клуба
- выводы и ограничения в конце ноутбука

## Как запустить
```bash
pip install -r requirements.txt
jupyter notebook Final_Football_project_fixed.ipynb
```
Или откройте ноутбук в Google Colab и загрузите `transfermarkt-datasets.duckdb` в `/content/`.

## Структура
```
├── Final_Football_project_fixed.ipynb
├── requirements.txt
└── README.md
```
