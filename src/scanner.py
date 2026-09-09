import concurrent.futures
import ipaddress
import socket


RISKY_PORTS = {
    21: "FTP",
    23: "Telnet",
    139: "NetBIOS",
    445: "SMB",
    3389: "RDP",
    5900: "VNC",
    6379: "Redis",
}


def parse_ports(value):
    ports = set()

    for item in value.split(","):
        item = item.strip()

        if not item:
            continue

        if "-" in item:
            start, end = item.split("-", 1)
            ports.update(range(int(start), int(end) + 1))
        else:
            ports.add(int(item))

    return sorted(
        port for port in ports
        if 1 <= port <= 65535
    )


def validate_network(target):
    network = ipaddress.ip_network(target, strict=False)

    if network.num_addresses > 1024:
        raise ValueError(
            "A rede possui mais de 1024 endereços. "
            "Reduza o CIDR para evitar uma varredura acidentalmente ampla."
        )

    return network


def check_port(host, port, timeout):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.settimeout(timeout)

            if sock.connect_ex((str(host), port)) == 0:
                return {
                    "host": str(host),
                    "port": port,
                    "risk": RISKY_PORTS.get(port, "normal"),
                    "status": "open",
                }

    except (socket.timeout, socket.error, OSError):
        return None

    return None


def scan_network(target, ports, timeout=0.7, workers=50):
    network = validate_network(target)
    hosts = list(network.hosts())
    findings = []

    with concurrent.futures.ThreadPoolExecutor(
        max_workers=workers
    ) as executor:

        tasks = [
            executor.submit(
                check_port,
                host,
                port,
                timeout
            )
            for host in hosts
            for port in ports
        ]

        for task in concurrent.futures.as_completed(tasks):
            result = task.result()

            if result:
                findings.append(result)

    return {
        "target": str(network),
        "assets_scanned": len(hosts),
        "ports_scanned": ports,
        "open_ports": sorted(
            findings,
            key=lambda item: (
                item["host"],
                item["port"],
            ),
        ),
    }


def calculate_score(scan_result):
    score = 100

    for finding in scan_result["open_ports"]:
        if finding["risk"] != "normal":
            score -= 8
        else:
            score -= 1

    return max(0, min(100, score))


def calculate_status(score):
    if score >= 80:
        return "PASS"

    if score >= 60:
        return "REVIEW"

    return "FAIL"
