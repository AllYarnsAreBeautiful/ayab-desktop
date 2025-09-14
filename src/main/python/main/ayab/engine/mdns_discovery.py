import contextlib
import zeroconf
import threading
import logging
from typing import Callable


class MdnsBrowser:
    """
    Explore Zeroconf services and manage them using a thread-safe dict
    """

    def __init__(self, service_type: str, update_callback: Callable[..., None]):
        self.service_type: str = service_type
        self.update_callback: Callable[..., None] = update_callback
        self.services: dict[str, zeroconf.ServiceInfo | None] = {}
        self.services_lock = threading.Lock()
        self.zeroconf_instance: zeroconf.Zeroconf | None = None
        self.browser: zeroconf.ServiceBrowser | None = None
        self.running = False
        self.__logger = logging.getLogger(type(self).__name__)

        self.listener: MdnsBrowser._ZeroconfListener = self._ZeroconfListener(self)

    # Inner class to act as the Zeroconf listener
    class _ZeroconfListener(zeroconf.ServiceListener):
        def __init__(self, parent_browser: "MdnsBrowser") -> None:
            self.parent_browser = parent_browser

        def add_service(
            self, zeroconf_instance: zeroconf.Zeroconf, service_type: str, name: str
        ) -> None:
            self.parent_browser._on_service_changed(
                zeroconf_instance, service_type, name, "added"
            )

        def update_service(
            self, zeroconf_instance: zeroconf.Zeroconf, service_type: str, name: str
        ) -> None:
            self.parent_browser._on_service_changed(
                zeroconf_instance, service_type, name, "updated"
            )

        def remove_service(
            self, zeroconf_instance: zeroconf.Zeroconf, service_type: str, name: str
        ) -> None:
            self.parent_browser._on_service_removed(
                zeroconf_instance, service_type, name
            )

    def _on_service_changed(
        self,
        zeroconf_instance: zeroconf.Zeroconf,
        service_type: str,
        name: str,
        change_type: str,
    ) -> None:
        """Callback called when a service is added or updated."""
        try:
            info: zeroconf.ServiceInfo | None = zeroconf_instance.get_service_info(
                service_type, name, timeout=3000
            )
            if info:
                self.__logger.info(f"Service {change_type}: {name}")
                with self.services_lock:
                    self.services[name] = info
                self.update_callback()
            else:
                self.__logger.warning(f"Unable to retrieve service {name} information")
        except Exception:
            self.__logger.exception(f"Error while fetching service {name}")

    def _on_service_removed(
        self, _zeroconf_instance: zeroconf.Zeroconf, _service_type: str, name: str
    ) -> None:
        """Callback called when a service is removed."""
        self.__logger.info(f"Service removed: {name}")
        should_notify = False
        with self.services_lock:
            if name in self.services:
                del self.services[name]
                should_notify = True
        if should_notify:
            self.update_callback()

    def start(self) -> None:
        """Start Zeroconf service browser."""
        if self.running:
            self.__logger.warning("MdnsBrowser already running.")
            return

        self.__logger.info(f"Starting service exploration for: {self.service_type}")
        try:
            self.zeroconf_instance = zeroconf.Zeroconf()
            self.browser = zeroconf.ServiceBrowser(
                self.zeroconf_instance,
                self.service_type,
                self.listener,
            )
            self.running = True
        except Exception:
            self.__logger.exception("Error while starting Zeroconf")
            self.stop()

    def stop(self) -> None:
        """Stop Zeroconf service exploration and clean up."""
        self.__logger.info("Shutting down MdnsBrowser...")
        if self.browser:
            self.browser.cancel()
            self.browser = None
        if self.zeroconf_instance:
            self.zeroconf_instance.close()
            self.zeroconf_instance = None
        self.running = False
        self.__logger.info("ServiceBrowser stopped.")

    def get_known_services(self) -> dict[str, zeroconf.ServiceInfo | None]:
        """Return known services."""
        with self.services_lock:
            return self.services.copy()

    def __del__(self) -> None:
        """Call the stop method when the instance is destroyed."""
        with contextlib.suppress(Exception):
            self.stop()
