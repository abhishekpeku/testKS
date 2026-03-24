from functools import lru_cache
from pathlib import Path

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "Investment Modelling Research Assistant"
    data_dir: Path = Field(default=Path("./data"))
    perplexity_api_key: str | None = None
    perplexity_model: str = "sonar-pro"
    openai_api_key: str | None = None
    trusted_domains: str = (
        "sec.gov,ifrs.org,fasb.org,cfainstitute.org,worldbank.org,imf.org"
    )
    code_include_extensions: str = ".py,.md,.txt,.yaml,.yml,.json"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    @property
    def trusted_domain_list(self) -> list[str]:
        return [item.strip().lower() for item in self.trusted_domains.split(",") if item.strip()]

    @property
    def code_extensions(self) -> list[str]:
        return [item.strip().lower() for item in self.code_include_extensions.split(",") if item.strip()]


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.data_dir.mkdir(parents=True, exist_ok=True)
    return settings
