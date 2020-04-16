# BooksCorpus

Based on the working of [0], including some fixtures and the integration of proxy usage due to the limitations of SmashWords, which only supports 100 requests per day.
The purpose of this repository is to replicate the Toronto BooksCorpus dataset. To this end, it scrapes and downloads books from Smashwords, the source of the original dataset. Similarly, all books are written in English and contain at least 20k words.

## Requirements

Al requirements are installed by calling `pip install --user -r requirements.txt`.

## Usage

```bash
python get_books.py
python download_books.py
python preprocess_books.py
```

[0] https://github.com/sgraaf/Replicate-Toronto-BookCorpus