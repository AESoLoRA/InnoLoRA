from typing import List, Dict
import os
import urllib.request
from urllib.error import URLError, HTTPError
from socket import timeout
from sys import stderr

from tqdm import tqdm
from libgen_api import Request, search, fetch
from bs4 import BeautifulSoup


# The library silently hangs (for minutes) if the mirror is unavailable.
# TODO: patch it to have a reasonable timeout and raise a descriptive exception.
fetch.LIBGEN_URL = 'https://libgen.is/search.php?'

FETCH_EXT = 'pdf'


def filename(s: str) -> str:
    return ''.join(c for c in s if c.isalnum() or c in "-_ .")


class DomainAwareDownloader:
    def __init__(self):
        self.fails: Dict[str, int] = {}
        self.trust_threshold = 2

    @staticmethod
    def domain(s: str) -> str:
        return '/'.join(s.split('/')[:3])

    def reorder_urls(self, urls: List[str]) -> List[str]:
        return sorted(urls, key=lambda u: self.fails.get(self.domain(u), 0))

    def try_download(self, name: str, urls: List[str]) -> None:
        # A-la `mkdir -p`
        try:
            os.mkdir('books')
        except FileExistsError:
            pass

        urls = self.reorder_urls(urls)

        data = None
        for url in urls:
            domain = self.domain(url)
            try:
                with urllib.request.urlopen(url, timeout=5) as conn:
                    data = conn.read()
            except (URLError, HTTPError) as e:
                print(f'\rSkipped mirror {domain} for: {e.reason}', file=stderr)
                self.fails[domain] = 1 + self.fails.get(domain, 0)
            except timeout:
                # This one occurs when the timeout is specifically in the _read_ opration.
                print(f'\rThe mirror {domain} was reached but failed to read from...', file=stderr)
            except Exception as e:
                print(f'\rUnexpected exception: {e} (type {type(e)}) when trying {domain}. '
                      'Will try another mirror...', file=stderr)
            else:
                break

        if not data:
            raise RuntimeError(f'No mirror worked for "{name}"')

        name = filename(name)
        with open(f'books/{name}.{FETCH_EXT}', 'wb') as f:
            f.write(data)


def get_librarylol_downloadables(s: str) -> List[str]:
    with urllib.request.urlopen(s, timeout=3) as conn:
        soup = BeautifulSoup(conn.read())
    ans = [a.get('href') for a in soup.find_all('a')]
    return [href for href in ans if href]


if __name__ == '__main__':
    req = Request('Haskell programming', num_results=1000)
    ress = search(req).filter(
        {'Extension': FETCH_EXT},
        exact_match=False  # Extremely misleading but must specify this for post-search filter
    )

    downloader = DomainAwareDownloader()
    for res in tqdm(ress):
        assert res.mirror_1.startswith('http://library.lol/')
        try:
            downloader.try_download(res.title, get_librarylol_downloadables(res.mirror_1))
        except RuntimeError as e:
            print(f'Exception with {res.title}:', e, file=stderr)
    print('FYI, detected failures:', downloader.fails)
