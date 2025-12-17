import argparse
import time
import random
from scanner.orchestrator import PortScanOrchestrator


def get_scan_profile(mode):
    """
    Defines scan behavior based on mode
    """
    if mode == "stealth":
        return {
            "workers": 20,
            "timeout": 3,
            "delay": (0.2, 0.6)
        }
    elif mode == "aggressive":
        return {
            "workers": 300,
            "timeout": 0.5,
            "delay": (0, 0)
        }
    else:  # baseline
        return {
            "workers": 100,
            "timeout": 1,
            "delay": (0, 0)
        }


def main():
    parser = argparse.ArgumentParser(
        description="Adaptive Network Reconnaissance Tool (Educational Use Only)"
    )

    parser.add_argument(
        "target",
        help="Target IP address or hostname"
    )

    parser.add_argument(
        "-s", "--start",
        type=int,
        default=1,
        help="Start port (default: 1)"
    )

    parser.add_argument(
        "-e", "--end",
        type=int,
        default=1024,
        help="End port (default: 1024)"
    )

    parser.add_argument(
        "--mode",
        choices=["baseline", "aggressive", "stealth"],
        default="baseline",
        help="Scan mode (baseline | aggressive | stealth)"
    )

    parser.add_argument(
        "-b", "--banner",
        action="store_true",
        help="Enable banner grabbing"
    )

    args = parser.parse_args()

    profile = get_scan_profile(args.mode)

    print(f"\n🔍 Scan mode: {args.mode.upper()}")
    print(f"Target: {args.target}")
    print(f"Port range: {args.start}-{args.end}\n")

    ports = list(range(args.start, args.end + 1))

    orchestrator = PortScanOrchestrator(
        target=args.target,
        ports=ports,
        timeout=profile["timeout"],
        grab_banners=args.banner,
        workers=profile["workers"]
    )

    results = []

    # Optional stealth delay handling
    for chunk_start in range(0, len(ports), 50):
        chunk = ports[chunk_start:chunk_start + 50]
        orchestrator.ports = chunk
        results.extend(orchestrator.run())

        if profile["delay"] != (0, 0):
            time.sleep(random.uniform(*profile["delay"]))

    if not results:
        print("❌ No open ports found.")
        return

    for r in sorted(results, key=lambda x: x["port"]):
        print(f"[+] Port {r['port']} OPEN ({r['service']})")
        if r["banner"]:
            print(f"    Banner: {r['banner'][:100]}")

    print(f"\n✅ Scan complete. Open ports found: {len(results)}")


if __name__ == "__main__":
    main()
