from pathlib import Path

from pydantic_settings import BaseSettings, SettingsConfigDict

BACKEND_DIR = Path(__file__).resolve().parent.parent.parent


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=BACKEND_DIR / ".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    app_name: str = "Mammoth Hockey Ops Dashboard"
    debug: bool = False
    database_path: str = "data/mammoth_ops.db"
    frontend_dir: str = "../frontend"
    nhl_team_abbr: str = "UTA"
    nhl_default_season: str = "20262027"

    @property
    def resolved_database_path(self) -> Path:
        path = Path(self.database_path)
        if not path.is_absolute():
            path = BACKEND_DIR / path
        return path

    @property
    def resolved_frontend_dir(self) -> Path:
        path = Path(self.frontend_dir)
        if not path.is_absolute():
            path = BACKEND_DIR / path
        return path.resolve()


settings = Settings()
