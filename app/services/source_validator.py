from app.config import get_settings


class SourceValidator:
    def __init__(self) -> None:
        self.trusted_domains = get_settings().trusted_domain_list

    def classify(self, domain: str) -> str:
        for trusted in self.trusted_domains:
            if domain == trusted or domain.endswith(f".{trusted}"):
                return "official"
        return "unverified"
