# Cybersecurity Exposure Platform

Plataforma básica para validação defensiva de exposição de rede.

## Recursos

- Varredura TCP de redes autorizadas;
- Identificação de portas abertas;
- Classificação simples de serviços sensíveis;
- Integração opcional com SonicWall;
- Consulta opcional ao Zabbix;
- Endpoint Prometheus;
- Dashboard Grafana;
- Relatório JSON;
- Execução por CMD, PowerShell, Linux ou Docker.

## Importante

Este projeto deve ser utilizado somente em redes próprias ou com autorização explícita.

Ele não explora vulnerabilidades, não tenta senhas, não altera regras de firewall e não executa payloads.

Uma porta aberta não prova a existência de uma CVE. O resultado deve ser tratado como indicador de exposição que precisa de validação adicional.

## Instalação

Crie um ambiente virtual:

```bash
python -m venv .venv
