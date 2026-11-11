import re
import sys
from urllib.parse import urlparse

URL_RE = re.compile(r"https?://[^\s\"'<>]+", re.IGNORECASE)
EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
IPV4_RE = re.compile(
    r"\b(?:(?:25[0-5]|2[0-4]\d|1?\d?\d)\.){3}(?:25[0-5]|2[0-4]\d|1?\d?\d)\b"
)
DOMAIN_RE = re.compile(
    r"\b(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z]{2,24}\b", re.IGNORECASE
)
HASH_RES = {
    "MD5": re.compile(r"\b[a-fA-F0-9]{32}\b"),
    "SHA1": re.compile(r"\b[a-fA-F0-9]{40}\b"),
    "SHA256": re.compile(r"\b[a-fA-F0-9]{64}\b"),
}
FILE_EXTENSIONS = {
    "exe", "dll", "bat", "txt", "zip", "pdf", "doc", "docx", "xls", "xlsx",
    "js", "py", "png", "jpg", "ps1", "sys", "dat", "sh", "log", "ini",
}


def refang(text):
    """Rimette in forma normale gli indicatori 'defangati'."""
    text = text.replace("[.]", ".")
    text = text.replace("(.)", ".")
    text = text.replace("[:]", ":")
    text = text.replace("[@]", "@")
    text = re.sub(r"hxxp", "http", text, flags=re.IGNORECASE)
    return text


def extract(text):
    """Cerca gli IoC nel testo e restituisce un dizionario di insiemi."""
    text = refang(text)

    urls = {u.rstrip(".,;:)]}'\"") for u in URL_RE.findall(text)}
    emails = set(EMAIL_RE.findall(text))
    ips = set(IPV4_RE.findall(text))

    # Per cercare i domini tolgo prima URL ed email, già trovati.
    rest = URL_RE.sub(" ", text)
    rest = EMAIL_RE.sub(" ", rest)

    domains = set()
    for url in urls:
        host = urlparse(url).hostname
        if host and not IPV4_RE.fullmatch(host):
            domains.add(host)
    for d in DOMAIN_RE.findall(rest):
        if d.split(".")[-1].lower() not in FILE_EXTENSIONS:
            domains.add(d.lower())

    result = {"URL": urls, "Dominio": domains, "IPv4": ips}
    for name, regex in HASH_RES.items():
        result[name] = {h.lower() for h in regex.findall(text)}
    result["Email"] = emails
    return result


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 ioc_extractor.py <file>")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        text = f.read()

    for name, values in extract(text).items():
        if values:
            print(f"[{name}]")
            for value in sorted(values):
                print(f"  {value}")


if __name__ == "__main__":
    main()
