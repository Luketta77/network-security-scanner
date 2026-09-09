from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import start_http_server


security_score = Gauge(
    "security_validation_score",
    "Score atual da validação de segurança",
)

assets_scanned = Gauge(
    "security_assets_scanned",
    "Quantidade de ativos analisados",
)

open_ports_total = Gauge(
    "security_open_ports_total",
    "Quantidade de portas abertas encontradas",
)

risky_ports_total = Gauge(
    "security_risky_ports_total",
    "Quantidade de portas classificadas como sensíveis",
)

integration_status = Gauge(
    "security_integration_status",
    "Status da integração: 1 conectado, 0 indisponível",
    ["integration"],
)

validation_runs_total = Counter(
    "security_validation_runs_total",
    "Quantidade de validações executadas",
)


def update_metrics(
    scan_result,
    score,
    sonicwall_connected,
    zabbix_connected,
):
    findings = scan_result["open_ports"]

    risky_findings = [
        item for item in findings
        if item["risk"] != "normal"
    ]

    security_score.set(score)
    assets_scanned.set(scan_result["assets_scanned"])
    open_ports_total.set(len(findings))
    risky_ports_total.set(len(risky_findings))

    integration_status.labels("sonicwall").set(
        1 if sonicwall_connected else 0
    )

    integration_status.labels("zabbix").set(
        1 if zabbix_connected else 0
    )

    validation_runs_total.inc()


def start_metrics_server(port):
    start_http_server(port)
