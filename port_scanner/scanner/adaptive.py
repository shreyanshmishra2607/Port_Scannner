def expand_ports(open_ports):
    expanded = set(open_ports)
    for port in open_ports:
        if port in (80, 443):
            expanded.update(range(8000, 8100))
        if port == 22:
            expanded.update(range(20, 30))
    return sorted(expanded)
