def calculate_risk(findings):
    score = 0
    for f in findings:
        if f["service"] in ("FTP", "Telnet"):
            score += 3
        if f.get("banner"):
            score += 2
    return min(score, 10)
