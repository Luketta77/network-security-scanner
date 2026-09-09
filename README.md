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

Windows:

bat


.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
Linux/macOS:

bash


source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
Executar no Windows
bat


scripts\validate.bat 192.168.1.0/24
Executar com Python
bash


python src/main.py
Métricas
Com o programa executando, acesse:

text


http://localhost:9108/metrics
Grafana e Prometheus
Inicie os serviços:

bash


docker compose up -d
Acesse:

text


Grafana: http://localhost:3000
Prometheus: http://localhost:9090
O usuário inicial padrão do Grafana normalmente é:

text


admin
Altere a senha no primeiro acesso.

SonicWall
Ative no arquivo .env:

env


SONICWALL\_ENABLED=true
SONICWALL\_BASE\_URL=https://192.168.1.1
SONICWALL\_API\_PATH=/api/sonicos
SONICWALL\_USERNAME=readonly\_user
SONICWALL\_PASSWORD=senha\_segura
SONICWALL\_VERIFY\_TLS=false
``
O endpoint utilizado pelo exemplo é configurável. Confirme no Swagger/API do seu SonicOS qual rota de leitura deve ser usada.

Zabbix
Ative no arquivo .env:

env


ZABBIX\_ENABLED=true
ZABBIX\_API\_URL=https://zabbix.example.com/zabbix/api\_jsonrpc.php
ZABBIX\_API\_TOKEN=seu\_token
ZABBIX\_VERIFY\_TLS=true
O projeto consulta a versão da API do Zabbix para testar a conectividade.

Limitações restantes
Mesmo com SonicWall, Zabbix e Grafana, este projeto ainda não:

Confirma CVEs;
Faz análise completa de versão de serviços;
Avalia código de aplicações;
Testa autenticação;
Analisa vulnerabilidades UDP;
Substitui um scanner de vulnerabilidades;
Substitui uma auditoria profissional;
Garante que um serviço exposto seja vulnerável.
As integrações melhoram o contexto e a observabilidade. Elas não transformam automaticamente uma varredura de portas em um scanner completo de vulnerabilidades.




## Como executar

Na primeira execução:

```bat

copy .env.example .env
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
scripts\validate.bat 192.168.1.0/24
Em outro terminal, suba o Grafana e o Prometheus:

bash


docker compose up -d
Depois abra:

text


http://localhost:3000
O fluxo ficará assim:

text


[+] Starting Security Validation...
[+] Discovering assets...
[+] Checking exposed ports...
[+] Evaluating risk...
[+] Connecting to SonicWall...
[+] Checking Zabbix API...
[+] Publishing Prometheus metrics...
[+] Validating security baseline...

Security Score: 92/100
Status: PASS

[+] Report saved to: reports/security-report.json
[+] Metrics available on port 9108

## Instalação

Crie um ambiente virtual:

```bash
python -m venv .venv
