import requests


class ZabbixClient:
    def __init__(self, api_url, token, verify_tls=True):
        self.api_url = api_url
        self.token = token
        self.verify_tls = verify_tls
        self.request_id = 0

    def call(self, method, params=None):
        self.request_id += 1

        response = requests.post(
            self.api_url,
            headers={
                "Content-Type": "application/json-rpc",
                "Authorization": f"Bearer {self.token}",
            },
            json={
                "jsonrpc": "2.0",
                "method": method,
                "params": params or {},
                "id": self.request_id,
            },
            timeout=15,
            verify=self.verify_tls,
        )

        response.raise_for_status()
        payload = response.json()

        if "error" in payload:
            raise RuntimeError(payload["error"])

        return payload.get("result")

    def health_check(self):
        try:
            version = self.call("apiinfo.version")

            return {
                "connected": True,
                "version": version,
            }

        except (
            requests.RequestException,
            RuntimeError,
        ) as error:
            return {
                "connected": False,
                "error": str(error),
            }

    def list_hosts(self):
        return self.call(
            "host.get",
            {
                "output": [
                    "hostid",
                    "host",
                    "name",
                    "status",
                ],
                "limit": 1000,
            },
        )
