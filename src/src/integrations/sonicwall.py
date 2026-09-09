import requests


class SonicWallClient:
    def __init__(
        self,
        base_url,
        api_path,
        username,
        password,
        verify_tls=True,
    ):
        self.base_url = base_url.rstrip("/")
        self.api_path = api_path.strip("/")
        self.username = username
        self.password = password
        self.verify_tls = verify_tls

    def get(self, resource):
        url = f"{self.base_url}/{self.api_path}/{resource.lstrip('/')}"

        response = requests.get(
            url,
            auth=(self.username, self.password),
            headers={
                "Accept": "application/json",
            },
            timeout=15,
            verify=self.verify_tls,
        )

        response.raise_for_status()

        return response.json()

    def health_check(self):
        try:
            data = self.get("status")
            return {
                "connected": True,
                "data": data,
            }

        except requests.RequestException as error:
            return {
                "connected": False,
                "error": str(error),
            }
