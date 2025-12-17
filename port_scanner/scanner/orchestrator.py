from concurrent.futures import ThreadPoolExecutor, as_completed
from scanner.core import scan_port
from scanner.banner import grab_banner
from scanner.services import COMMON_SERVICES


class PortScanOrchestrator:
    def __init__(self, target, ports, timeout=1, grab_banners=False, workers=100):
        self.target = target
        self.ports = ports
        self.timeout = timeout
        self.grab_banners = grab_banners
        self.workers = workers
        self.results = []

    def run(self):
        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = {
                executor.submit(scan_port, self.target, port, self.timeout): port
                for port in self.ports
            }

            for future in as_completed(futures):
                port = futures[future]
                try:
                    is_open = future.result()
                    if is_open:
                        service = COMMON_SERVICES.get(port, "Unknown")
                        banner = None

                        if self.grab_banners:
                            banner = grab_banner(self.target, port)

                        self.results.append({
                            "port": port,
                            "service": service,
                            "banner": banner
                        })
                except Exception:
                    continue

        return self.results
