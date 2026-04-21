"""Project entrypoint for the Modular RAG MCP Server."""

from core.settings import SettingsError, load_settings
from observability.logger import get_logger


LOGGER = get_logger(__name__)


def main(config_path: str = "config/settings.yaml") -> int:
    """Load the project settings and fail fast on invalid configuration."""
    try:
        settings = load_settings(config_path)
    except SettingsError as exc:
        LOGGER.error("Failed to load settings: %s", exc)
        return 1

    LOGGER.info(
        "Loaded settings successfully: llm=%s embedding=%s vector_store=%s",
        settings.llm["provider"],
        settings.embedding["provider"],
        settings.vector_store["provider"],
    )
    print("Modular RAG MCP Server settings loaded successfully.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
