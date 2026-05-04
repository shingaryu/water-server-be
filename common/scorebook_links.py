import os
from urllib.parse import parse_qsl, urlencode, urlsplit, urlunsplit


DEFAULT_SCOREBOOK_GROUP_NAME = "Water Cooler"
LOCAL_SCOREBOOK_PATH = "/badminton-scorebook"
SCOREBOOK_TABS = {"record", "stats", "settings"}


def scorebook_group_name() -> str:
    return os.getenv("SCOREBOOK_GROUP_NAME", DEFAULT_SCOREBOOK_GROUP_NAME).strip() or DEFAULT_SCOREBOOK_GROUP_NAME


def normalize_scorebook_tab(tab: str | None) -> str:
    return tab if tab in SCOREBOOK_TABS else "record"


def scorebook_local_path(tab: str | None = None) -> str:
    return add_query_params(
        LOCAL_SCOREBOOK_PATH,
        {
            "tab": normalize_scorebook_tab(tab),
            "group": scorebook_group_name(),
        },
    )


def scorebook_target_url(base_url: str, tab: str | None = None) -> str:
    scorebook_app_url = os.getenv("SCOREBOOK_APP_URL", "").strip()
    target = scorebook_app_url or f"{base_url.rstrip('/')}{LOCAL_SCOREBOOK_PATH}"
    return add_query_params(
        target,
        {
            "tab": normalize_scorebook_tab(tab),
            "group": scorebook_group_name(),
        },
    )


def add_query_params(url: str, params: dict[str, str]) -> str:
    parts = urlsplit(url)
    query = dict(parse_qsl(parts.query, keep_blank_values=True))
    query.update({key: value for key, value in params.items() if value})
    return urlunsplit((parts.scheme, parts.netloc, parts.path, urlencode(query), parts.fragment))
