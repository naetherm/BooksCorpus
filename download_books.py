import os
from concurrent.futures import ThreadPoolExecutor
from itertools import count, cycle, repeat
from pathlib import Path

from cachecontrol import CacheControl
from requests import Session
from tqdm import tqdm
import logging

from utils import dump, get, get_book_id, get_headers, load, mkdirs, read, sanitize_file, write, get_proxies

LOGGER = logging.getLogger(__name__)

SECRET_KEY = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

NB_RETRIES = 3


def main():
  # create dirs
  root_dir = Path(__file__).resolve().parents[0]
  if SECRET_KEY:
    data_dir = Path('/data/')
    dump_dir = Path('/data/dump/')
  else:
    data_dir = root_dir / 'data'
    dump_dir = root_dir / 'dump'
  mkdirs(data_dir, dump_dir)

  # load book_download_urls
  book_download_urls = read(data_dir / 'book_download_urls.txt').splitlines()

  # remove any books that have already been downloaded
  book_download_urls = ['https://www.smashwords.com'+url for url in book_download_urls if not (data_dir / f'{get_book_id(url)}.txt').exists()]

  if book_download_urls:
    # keep only the first 500 (as smashwords blocks the IP-address after 500 requests)
    book_download_urls = book_download_urls #[:500]

    # get headers (user-agents)
    headers = get_headers(root_dir / 'user-agents.txt')

    # initialize cache-controlled session
    session = CacheControl(Session())

    # get the books (concurrently)
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
      for nb_retry in count(1):
        # break if all book_download_urls successful
        if not book_download_urls:
          break

        # break if max number of retries exceeded
        if nb_retry > NB_RETRIES:
          LOGGER.warning(f'Could not download {len(book_download_urls)} books after {NB_RETRIES} retries.')
          break

        # maintain a list of failed downloads (for future retries)
        failed_book_download_urls = []

        proxies=get_proxies()

        # get the book_responses
        book_responses = list(tqdm(executor.map(get, book_download_urls, repeat(session), cycle(headers), cycle(proxies)), total=len(book_download_urls), desc='Getting books'))

        # dump the book_responses
        dump(book_responses, 'book_responses.pkl', dump_dir=dump_dir)

        for book_url, book_r in zip(book_download_urls, book_responses):
          #print("Book content: {}".format(book_r.content))
          if book_r is not None:
            if book_r.status_code == 200:
              book_r.encoding = 'utf-8'

              # write the content to disk
              write(book_r.content, data_dir / f'{get_book_id(book_url)}.txt')
            else:
              failed_book_download_urls.append(book_url)
              LOGGER.warning(f'Request failed for {book_url}: status code [{book_r.status_code}]')
          else:
            LOGGER.warning(f"The request for the book_url '{book_url}' was None.")

        book_download_urls = failed_book_download_urls

if __name__ == '__main__':
  main()
