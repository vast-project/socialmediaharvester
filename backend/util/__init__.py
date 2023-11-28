import urllib.parse


def urlencode(s: str, safe: str = "") -> str:
    # result = s.replace("'", "’")
    # result = s.replace("\n", "%0a")
    return urllib.parse.quote_plus(s, safe=safe)


def urldecode(s: str) -> str:
    result = urllib.parse.unquote_plus(s)
    return result.replace("%0a", "\n")
