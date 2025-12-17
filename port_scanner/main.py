import argparse
from scanner.orchestrator import PortScanOrchestrator


def parse_ports(start, end):
    return list(range(start, end + 1))


def main():
    parser = argparse.ArgumentParser(
        description="Python Network Port Scanner (Educational Use Only)"
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
        "-t", "--timeout",
        type=int,
        default=1,
        help="Socket timeout in seconds"
    )

    parser.add_argument(
        "-b", "--banner",
        action="store_true",
        help="Enable banner grabbing"
    )

    parser.add_argument(
        "-w", "--workers",
        type=int,
        default=100,
        help="Number of concurrent threads"
    )

    args = parser.parse_args()

    ports = parse_ports(args.start, args.end)

    orchestrator = PortScanOrchestrator(
        target=args.target,
        ports=ports,
        timeout=args.timeout,
        grab_banners=args.banner,
        workers=args.workers
    )

    print(f"\n🔍 Scanning {args.target} ({args.start}-{args.end})...\n")

    results = orchestrator.run()

    if not results:
        print("❌ No open ports found.")
        return

    for result in sorted(results, key=lambda x: x["port"]):
        print(f"[+] Port {result['port']} OPEN ({result['service']})")
        if result["banner"]:
            print(f"    Banner: {result['banner'][:100]}")

    print(f"\n✅ Scan complete. Open ports found: {len(results)}")


if __name__ == "__main__":
    main()
