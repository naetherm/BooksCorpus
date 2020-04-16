
import os
from pathlib import Path
from tqdm import tqdm
from utils import bytes2text, read, text2sentences

SECRET_KEY = os.environ.get('AM_I_IN_A_DOCKER_CONTAINER', False)

def main():
  # create dirs
  root_dir = Path(__file__).resolve().parents[0]
  if SECRET_KEY:
    data_dir = Path('/data/')
  else:
    data_dir = root_dir / 'data'

  if not data_dir.exists():
    raise RuntimeError(f'data_dir does not exist: {str(data_dir)}')

  # get book_files
  book_files = sorted(data_dir.glob('*.txt'))

  with open(data_dir / 'replica.txt', 'w', encoding='utf-8') as fout:
    for book_file in tqdm(book_files, total=len(book_files), desc='Pre-processing books'):
      book_bytes = read(book_file, mode='rb')
      book_text = bytes2text(book_bytes)
      book_sentences = text2sentences(book_text)
      fout.write(book_sentences)
      fout.write('\n\n\n')  # 3 empty lines between distinct books


if __name__ == '__main__':
  main()
