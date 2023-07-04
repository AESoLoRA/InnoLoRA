from typing import List, Dict
import os
import urllib.request
from socket import timeout

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
        urls_trusteds = [
                (url, bool(self.fails.get(self.domain(url), 0) < self.trust_threshold))
                for url in urls
            ]
        trusted_urls = [url for url, is_trusted in urls_trusteds if is_trusted]
        untrusted_urls = [url for url, is_trusted in urls_trusteds if not is_trusted]
        return trusted_urls + untrusted_urls

    def try_download(self, name: str, urls: List[str]) -> None:
        # A-la `mkdir -p`
        try:
            os.mkdir('books')
        except FileExistsError:
            pass

        urls = self.reorder_urls(urls)

        data = None
        for url in urls:
            try:
                with urllib.request.urlopen(url, timeout=5) as conn:
                    data = conn.read()
            except urllib.error.URLError as e:
                # I only want to catch actual timeout errors here. But can't specify
                # that in the `except` because `urllib` wraps the actual error in its
                # own type...
                if not isinstance(e.reason, TimeoutError):
                    raise

                domain = self.domain(url)
                self.fails[domain] = 1 + self.fails.get(domain, 0)
                continue
            except TimeoutError:
                # This one occurs when the timeout is specifically in the _read_ opration.
                print(f'The mirror {url} was reached but failed to read from...')
                continue
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
        downloader.try_download(res.title, get_librarylol_downloadables(res.mirror_1))
    print('FYI, detected failures:', downloader.fails)
