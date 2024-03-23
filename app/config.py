from typing import Any, Tuple, Type

from pydantic.fields import FieldInfo
from pydantic_settings import (
    BaseSettings,
    SettingsConfigDict,
    EnvSettingsSource,
    DotEnvSettingsSource,
    PydanticBaseSettingsSource,
)


class CommaSeparatedEnvSource(EnvSettingsSource):
    def prepare_field_value(self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool) -> Any:
        if field_name == "telegram_usernames":
            return value.split(",")
        return super().prepare_field_value(field_name, field, value, value_is_complex)


class CommaSeparatedDotEnvSource(DotEnvSettingsSource):
    def prepare_field_value(self, field_name: str, field: FieldInfo, value: Any, value_is_complex: bool) -> Any:
        if field_name == "telegram_usernames":
            return value.split(",")
        return super().prepare_field_value(field_name, field, value, value_is_complex)


class Settings(BaseSettings):
    debug: bool = False

    app_base_url: str

    telegram_bot_token: str
    telegram_usernames: list[str]

    model_config = SettingsConfigDict(env_file=".env")

    def telegram_webhook_path(self) -> str:
        return f"/bot/{self.telegram_bot_token}"

    def telegram_webhook_url(self) -> str:
        return f"{self.app_base_url}{self.telegram_webhook_path()}"

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            CommaSeparatedEnvSource(settings_cls),
            CommaSeparatedDotEnvSource(settings_cls, env_file="app/.env"),
        )


settings = Settings()
