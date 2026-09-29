"""Download the open datasets used here (not redistributed in this repository).

SIB-200 (CC BY-SA 4.0): test/dev splits for English + 24 Indian-language sets, ~2.5 MB.
MASSIVE v1.1 (CC BY 4.0): one tarball, ~40 MB; the 8 locale files used are extracted.
"""
import tarfile
import urllib.request
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / 'data'
LANGS = ('eng_Latn asm_Beng awa_Deva ben_Beng bho_Deva guj_Gujr hin_Deva hne_Deva kan_Knda kas_Arab kas_Deva '
         'mag_Deva mai_Deva mal_Mlym mar_Deva mni_Beng npi_Deva ory_Orya pan_Guru san_Deva sat_Olck snd_Arab '
         'tam_Taml tel_Telu urd_Arab').split()
MASSIVE = 'https://amazon-massive-nlu-dataset.s3.amazonaws.com/amazon-massive-dataset-1.1.tar.gz'
LOCALES = ['en-US', 'hi-IN', 'te-IN', 'ta-IN', 'kn-IN', 'ml-IN', 'bn-BD', 'ur-PK']

for lang in LANGS:
    (DATA / lang).mkdir(parents=True, exist_ok=True)
    for name in ('test.tsv', 'dev.tsv', 'labels.txt'):
        url = f'https://huggingface.co/datasets/Davlan/sib200/resolve/main/data/{lang}/{name}'
        (DATA / lang / name).write_bytes(urllib.request.urlopen(url, timeout=60).read())
tar_path = DATA / 'massive' / 'amazon-massive-dataset-1.1.tar.gz'
tar_path.parent.mkdir(parents=True, exist_ok=True)
urllib.request.urlretrieve(MASSIVE, tar_path)
with tarfile.open(tar_path) as tar:
    tar.extractall(DATA / 'massive', members=[m for m in tar.getmembers()
                                              if any(m.name.endswith(f'/{loc}.jsonl') for loc in LOCALES)],
                   filter='data')
print('data ready in', DATA)
