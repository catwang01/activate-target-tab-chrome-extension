import platform


class NotSupportPlatform(Exception):
    pass


def detect_system():
    p = platform.system().lower()
    if p == "darwin":
        return "MacOs"
    elif p == "win32":
        return "Windows"
    else:
        raise NotSupportPlatform()