import json
import logging
from PySide6.QtNetwork import QNetworkAccessManager, QNetworkRequest, QNetworkReply
import semver

from . import utils


class VersionChecker:
    REPO = "AllYarnsAreBeautiful/ayab-desktop"

    logger: logging.Logger
    _current_version: str
    _network_manager: QNetworkAccessManager | None
    _version_check_reply: QNetworkReply | None

    def __init__(self, current_version: str) -> None:
        self.logger = logging.getLogger(type(self).__name__)
        self._current_version = current_version

    def start_background_check(self) -> None:
        self._network_manager = QNetworkAccessManager()
        self._version_check_reply = self._network_manager.get(
            QNetworkRequest(f"https://api.github.com/repos/{self.REPO}/releases/latest")
        )
        self._version_check_reply.finished.connect(self.version_check_finished)

    def is_newer(self, latest_version: str) -> bool:
        try:
            v_current: semver.Version = semver.Version.parse(self._current_version)
        except Exception:
            self.logger.warning("Error while parsing current version", exc_info=True)
            return False

        try:
            v_latest: semver.Version = semver.Version.parse(latest_version)
        except Exception:
            self.logger.warning("Error while parsing latest version", exc_info=True)
            return False

        return v_latest > v_current

    def version_check_finished(self) -> None:
        try:
            if self._version_check_reply is None:  # should never happen, pleases mypy
                return

            if self._version_check_reply.error() != QNetworkReply.NetworkError.NoError:
                self.logger.warning(
                    "Network error while checking for new versions: %s",
                    self._version_check_reply.errorString(),
                )
                return

            data = self._version_check_reply.readAll()
            obj = json.loads(data.data())
            if not obj.get("draft", True) and not obj.get("prerelease", True):
                latest_version = obj.get("tag_name")
                url = obj.get("html_url")
                if latest_version is not None and url is not None and self.is_newer(latest_version):
                    utils.display_blocking_popup(
                        f"""<p>
                        A new version of the AYAB desktop software
                        has been released!<br>
                        You are using version
                        <strong>{self._current_version}</strong>;
                        you can download version <strong>{latest_version}</strong>
                        using this link:
                        <br/>
                        <a href='{url}'>{url}</a>
                        </p>"""
                    )
        finally:
            # make sure to free resources once done
            self._version_check_reply = None
            self._network_manager = None
