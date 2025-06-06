import zeroconf
import socket
import threading
import time
import logging

class MdnsBrowser:
    """
    Explore Zeroconf services and manage them using a thread-safe dict
    """
    def __init__(self, service_type: str):
        self.service_type : str = service_type
        self.services : dict [str, zeroconf.ServiceInfo | None] = {}
        self.services_lock = threading.Lock()
        self.zeroconf_instance : zeroconf.Zeroconf | None = None
        self.browser : zeroconf.ServiceBrowser | None = None
        self.running = False
        self.__logger = logging.getLogger(type(self).__name__)

        self.listener : MdnsBrowser._ZeroconfListener = self._ZeroconfListener(self)

    # Inner class to act as the Zeroconf listener
    class _ZeroconfListener(zeroconf.ServiceListener):
        def __init__(self, parent_browser : 'MdnsBrowser') -> None:
            self.parent_browser = parent_browser

        def add_service(self, zeroconf_instance: zeroconf.Zeroconf, type: str, name: str) -> None:
            self.parent_browser._on_service_changed(zeroconf_instance, type, name, "added")

        def update_service(self, zeroconf_instance: zeroconf.Zeroconf, type: str, name: str) -> None:
            self.parent_browser._on_service_changed(zeroconf_instance, type, name, "updated")

        def remove_service(self, zeroconf_instance: zeroconf.Zeroconf, type: str, name: str) -> None:
            self.parent_browser._on_service_removed(zeroconf_instance, type, name)

    def _on_service_changed(self, zeroconf_instance: zeroconf.Zeroconf, type: str, name: str, change_type: str) -> None:
        """Callback called when a service is added or updated."""
        info : zeroconf.ServiceInfo | None = zeroconf.ServiceInfo(type, name)
        try:
            info = zeroconf_instance.get_service_info(type, name, timeout=3000)
            if info:
                info = zeroconf_instance.get_service_info(type, name)
                self.__logger.info(f"Service {change_type}: {name}")
                with self.services_lock:
                    self.services[name] = info
            else:
                self.__logger.warning(f"Unable to retrieve service {name} information")
        except Exception as e:
            self.__logger.error(f"Error while fetching service {name}: {e}")


    def _on_service_removed(self, zeroconf_instance: zeroconf.Zeroconf, type: str, name: str) -> None:
        """Callback called when a service is removed."""
        self.__logger.info(f"Service removed: {name}")
        with self.services_lock:
            if name in self.services:
                del self.services[name]

    def _on_service_updated(self, zeroconf_instance: zeroconf.Zeroconf, type: str, name: str) -> None:
        """Callback called when a service's information is updated."""
        self.__logger.info(f"Service '{name}' of type '{type}' updated. Attempting to get new info...")
        try:
            # Re-fetch the service info as it might have changed
            info = zeroconf_instance.get_service_info(type, name, timeout=3000)

            if info:
                self.__logger.info(f"Successfully retrieved updated info for service: {name}")
                with self.services_lock:
                    self.services[name] = info # Overwrite with new info
            else:
                self.__logger.warning(f"Failed to retrieve updated information for service {name} (it might have disappeared or changed unexpectedly).")
        except Exception as e:
            self.__logger.error(f"Error during service info update for {name}: {e}")

    def start(self) -> None:
        """Start Zeroconf service browser."""
        if self.running:
            self.__logger.warning("MdnsBrowser already running.")
            return

        self.running = True
        self.__logger.info(f"Starting service exploration for: {self.service_type}")
        try:
            self.zeroconf_instance = zeroconf.Zeroconf()
            listener = zeroconf.ServiceBrowser(
                self.zeroconf_instance,
                self.service_type,
                self.listener,
            )
            self.browser = listener
        except Exception as e:
            self.__logger.error(f"Error while starting Zeroconf: {e}")
            self.stop()

    def stop(self) -> None:
        """Stop Zeroconf service exploration and clean up."""
        if not self.running:
            self.__logger.warning("MdnsBrowser not running.")
            return

        self.__logger.info("Shutting down MdnsBrowser...")
        if self.browser:
            self.browser.cancel()
        if self.zeroconf_instance:
            self.zeroconf_instance.close()
        self.running = False
        self.__logger.info("ServiceBrowser stopped.")

    def get_known_services(self) -> dict[str, zeroconf.ServiceInfo | None]:
        """Return known services."""
        with self.services_lock:
            return self.services.copy()

