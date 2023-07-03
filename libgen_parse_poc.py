from typing import List
import os
import urllib.request
from socket import timeout

from tqdm import tqdm
from libgen_api import Request, search, fetch
from bs4 import BeautifulSoup


# The library silently hangs (for minutes) if the mirror is unavailable.
# TODO: patch it to have a reasonable timeout and raise a descriptive exception.
fetch.LIBGEN_URL = 'https://libgen.is/search.php?'


def filename(s: str) -> str:
    return ''.join(c for c in s if c.isalnum() or c in "-_ .")


def try_download(name: str, urls: List[str]) -> None:
    # A-la `mkdir -p`
    try:
        os.mkdir('books')
    except FileExistsError:
        pass

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

            continue
        else:
            break

    if not data:
        raise RuntimeError(f'No mirror worked for "{name}", '
                           'or the book is too large, increase timeout')

    name = filename(name)
    with open(f'books/{name}', 'wb') as f:
        f.write(data)


def get_librarylol_downloadables(s: str) -> List[str]:
    with urllib.request.urlopen(s, timeout=3) as conn:
        soup = BeautifulSoup(conn.read())
    ans = [a.get('href') for a in soup.find_all('a')]
    return [href for href in ans if href]


if __name__ == '__main__':
    req = Request('Haskell programming', num_results=1000)
    ress = search(req).filter(
        {'Extension': 'epub'},
        exact_match=False  # Extremely misleading but must specify this for post-search filter
    )

    for res in tqdm(ress):
        assert res.mirror_1.startswith('http://library.lol/')
        try_download(res.title, get_librarylol_downloadables(res.mirror_1))
