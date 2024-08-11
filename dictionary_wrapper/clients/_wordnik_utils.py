import bs4 as bs


def _parse_xml(content: str) -> str:
    return bs.BeautifulSoup(content, "xml").text
