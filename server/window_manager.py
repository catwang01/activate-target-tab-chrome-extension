from log import setupLogger
from abc import ABCMeta, abstractmethod

logger = setupLogger(__name__)

class IWindowManager(metaclass=ABCMeta):

    @abstractmethod
    def activate_window(self, title: str) -> bool:
        pass

class WindowsWindowManager(IWindowManager):

    def activate_window(self, title: str) -> bool:
        logger.info(f"Detecting window: {title}")
        window = self._find_window(title)
        logger.info(f"Find a window: {window}")
        if window is None:
            logger.warning("Window can be not fojund")
            return False
        window.activate()
        return True

    def _find_window(self, keyword: str):
        import pyautogui
        import pywinctl as pwc

        pyautogui.press("alt")
        allWindows = pwc.getAllWindows()
        for window in allWindows:
            logger.debug(window)
            if isinstance(window.title, str) and keyword.lower() in window.title.lower():
                return window
        return None


class MacOsWindowManager(IWindowManager):

    def _is_evernote(self, app) -> bool:
        return app.localizedName() in {'Evernote', '印象笔记'}

    def activate_window(self, title: str) -> bool:
        from AppKit import NSWorkspace
        from Quartz import NSApplicationActivateIgnoringOtherApps
        
        current_app = NSWorkspace.sharedWorkspace().frontmostApplication()
        logger.debug(f"Current app: {current_app}")
        if self._is_evernote(current_app):
            logger.info("Skip for evernote")
            return False
        running_apps = NSWorkspace.sharedWorkspace().runningApplications()

        # Find the application with the specified window name
        target_app = None
        for app in running_apps:
            if app.localizedName() == title:
                target_app = app
                break

        if target_app:
            # Bring the application to the foreground
            target_app.activateWithOptions_(NSApplicationActivateIgnoringOtherApps)
            logger.info("window is activated")
            return True
        return False