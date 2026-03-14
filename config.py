from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FlightTime Athletics Athlete Development API"
    database_url: str = "sqlite+pysqlite:///./flighttime_athletics.db"
    uploads_dir: str = "uploads"
    app_base_url: str = "http://127.0.0.1:5173"
    cors_origins: str = "http://127.0.0.1:5173,http://localhost:5173,http://127.0.0.1:3000,http://localhost:3000"
    stripe_secret_key: str = ""
    square_payment_link_url: str = ""
    seed_demo_users: bool = False

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @property
    def cors_origins_list(self) -> list[str]:
        return [origin.strip() for origin in self.cors_origins.split(",") if origin.strip()]


settings = Settings()
