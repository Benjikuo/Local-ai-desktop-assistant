import webbrowser


def handle(url):
    webbrowser.open(url)
    return f"Opened {url}"
