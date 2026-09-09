import json
import os
import time
from datetime import datetime
from pathlib import Path

from dotenv import load_dotenv

from scanner import (
    calculate_score,
    calculate_status,
    parse_ports,
    scan_network,
)

from metrics_server import (
    start_metrics_server,
    update_metrics,
)

from integrations.sonicwall import SonicWallClient
from integrations.zabbix import ZabbixClient


def env_bool(name, default=False):
    value = os.getenv(name, str(default)).lower()
    return value in ("1", "true", "yes", "sim")


def save_report(report, path):
    output = Path(path)
    output.parent.mkdir(parents=True, exist_ok=True)

    with output.open("w", encoding="utf-8") as file:
        json.dump(
            report,
            file,
            indent=4,
            ensure_ascii=False,
        )


def main():
    load_dotenv()

    target = os.getenv("TARGET_CIDR", "192.168.1.0/24")
    ports = parse_ports(
        os.getenv(
            "SCAN_PORTS",
            "22,80,443,445,3389,8080",
        )
    )

    timeout = float(os.getenv("SCAN_TIMEOUT", "0.7"))
    workers = int(os.getenv("SCAN_WORKERS", "50"))
    metrics_port = int(os.getenv("METRICS_PORT", "9108"))
    report_path = os.getenv(
        "REPORT_PATH",
        "reports/security-report.json",
    )

    print()
    print("[+] Starting Security Validation...")
    print("[+] Discovering assets...")

    start_metrics_server(metrics_port)

    print(f"[+] Metrics available on port {metrics_port}")
    print(f"[+] Target: {target}")
    print(f"[+] Ports: {ports}")
    print("[+] Checking exposed ports...")

    scan_result = scan_network(
        target=target,
        ports=ports,
        timeout=timeout,
        workers=workers,
    )

    print("[+] Evaluating risk...")
    score = calculate_score(scan_result)
    status = calculate_status(score)

    sonicwall_result = {
        "enabled": False,
        "connected": False,
    }

    if env_bool("SONICWALL_ENABLED"):
        client = SonicWallClient(
            base_url=os.getenv("SONICWALL_BASE_URL"),
            api_path=os.getenv("SONICWALL_API_PATH", "/api/sonicos"),
            username=os.getenv("SONICWALL_USERNAME"),
            password=os.getenv("SONICWALL_PASSWORD"),
            verify_tls=env_bool(
                "SONICWALL_VERIFY_TLS",
                True,
            ),
        )

        sonicwall_result = client.health_check()
        sonicwall_result["enabled"] = True

    zabbix_result = {
        "enabled": False,
        "connected": False,
    }

    if env_bool("ZABBIX_ENABLED"):
        client = ZabbixClient(
            api_url=os.getenv("ZABBIX_API_URL"),
            token=os.getenv("ZABBIX_API_TOKEN"),
            verify_tls=env_bool(
                "ZABBIX_VERIFY_TLS",
                True,
            ),
        )

        zabbix_result = client.health_check()
        zabbix_result["enabled"] = True

    update_metrics(
        scan_result=scan_result,
        score=score,
        sonicwall_connected=sonicwall_result["connected"],
        zabbix_connected=zabbix_result["connected"],
    )

    report = {
        "generated_at": datetime.now().isoformat(
            timespec="seconds"
        ),
        "scan": scan_result,
        "security_score": score,
        "status": status,
        "integrations": {
            "sonicwall": sonicwall_result,
            "zabbix": zabbix_result,
        },
    }

    save_report(report, report_path)

    print()
    print(f"Security Score: {score}/100")
    print(f"Status: {status}")
    print()
    print(
        f"[+] Open ports found: "
        f"{len(scan_result['open_ports'])}"
    )
    print(
        f"[+] Report saved to: {report_path}"
    )
    print()

    # Mantém o endpoint /metrics disponível para o Prometheus.
    while True:
        time.sleep(60)


if __name__ == "__main__":
    main()
