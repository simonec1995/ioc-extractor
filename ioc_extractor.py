import re
import sys


def refang(text):
    """Rimette in forma normale gli indicatori 'defangati'."""
    text = text.replace("[.]", ".")
    text = text.replace("(.)", ".")
    text = text.replace("[:]", ":")
    text = text.replace("[@]", "@")
    text = re.sub(r"hxxp", "http", text, flags=re.IGNORECASE)
    return text


def main():
    if len(sys.argv) != 2:
        print("Uso: python3 ioc_extractor.py <file>")
        sys.exit(1)

    with open(sys.argv[1], encoding="utf-8") as f:
        text = f.read()

    print(refang(text))


if __name__ == "__main__":
    main()
