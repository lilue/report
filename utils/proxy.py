import report.settings


def proxy():
    if report.settings.USE_PROXY:
        return {}
    else:
        return {}
