from __future__ import annotations

from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Dict, List
from zoneinfo import ZoneInfo

from skyfield import almanac, almanac_east_asia
from skyfield.api import Loader


DEFAULT_TIMEZONE = "Asia/Shanghai"
EPHEMERIS_NAME = "de421.bsp"
SOLAR_TERM_NAMES = tuple(almanac_east_asia.SOLAR_TERMS_ZHS)
JIE_BOUNDARY_INDEX_TO_MONTH = {
    21: 1,
    23: 2,
    1: 3,
    3: 4,
    5: 5,
    7: 6,
    9: 7,
    11: 8,
    13: 9,
    15: 10,
    17: 11,
    19: 12,
}


def _cache_dir() -> Path:
    path = Path.home() / ".cache" / "lao-huangli" / "skyfield"
    path.mkdir(parents=True, exist_ok=True)
    return path


@lru_cache(maxsize=1)
def _loader() -> Loader:
    return Loader(str(_cache_dir()))


@lru_cache(maxsize=1)
def _timescale():
    return _loader().timescale()


@lru_cache(maxsize=1)
def _ephemeris():
    return _loader()(EPHEMERIS_NAME)


def _to_local(dt: datetime, timezone_name: str) -> datetime:
    tz = ZoneInfo(timezone_name)
    if dt.tzinfo is None:
        return dt.replace(tzinfo=tz)
    return dt.astimezone(tz)


def _format_local(dt: datetime) -> str:
    return dt.isoformat(timespec="seconds")


@lru_cache(maxsize=16)
def list_solar_terms_for_year(year: int, timezone_name: str = DEFAULT_TIMEZONE) -> List[Dict[str, object]]:
    tz = ZoneInfo(timezone_name)
    ts = _timescale()
    eph = _ephemeris()
    start = datetime(year - 1, 12, 1, tzinfo=tz).astimezone(timezone.utc)
    end = datetime(year + 1, 1, 31, 23, 59, 59, tzinfo=tz).astimezone(timezone.utc)
    times, indexes = almanac.find_discrete(
        ts.from_datetime(start),
        ts.from_datetime(end),
        almanac_east_asia.solar_terms(eph),
    )

    events: List[Dict[str, object]] = []
    for time_obj, index in zip(times, indexes):
        local_dt = time_obj.utc_datetime().astimezone(tz)
        events.append(
            {
                "index": int(index),
                "name": SOLAR_TERM_NAMES[int(index)],
                "at": local_dt,
            }
        )
    return events


def get_solar_term_window(dt: datetime, timezone_name: str = DEFAULT_TIMEZONE) -> Dict[str, object]:
    local_dt = _to_local(dt, timezone_name)
    events = list_solar_terms_for_year(local_dt.year, timezone_name)

    current_event = events[0]
    next_event = events[-1]
    for idx, event in enumerate(events):
        if event["at"] <= local_dt:
            current_event = event
            if idx + 1 < len(events):
                next_event = events[idx + 1]
            continue
        next_event = event
        break

    return {
        "current": current_event["name"],
        "currentIndex": current_event["index"],
        "currentAt": _format_local(current_event["at"]),
        "next": next_event["name"],
        "nextIndex": next_event["index"],
        "nextAt": _format_local(next_event["at"]),
        "precision": "astronomical",
        "calculationMode": "skyfield-jpl",
        "timezone": timezone_name,
        "note": "节气按 Skyfield + JPL 星历计算，时刻为本地时区结果",
    }


def get_jieqi_month_for_datetime(dt: datetime, timezone_name: str = DEFAULT_TIMEZONE) -> int:
    current_index = int(get_solar_term_window(dt, timezone_name)["currentIndex"])
    boundary_index = current_index if current_index in JIE_BOUNDARY_INDEX_TO_MONTH else (current_index - 1) % 24
    return JIE_BOUNDARY_INDEX_TO_MONTH[boundary_index]


def get_solar_term_occurrence(year: int, term_name: str, timezone_name: str = DEFAULT_TIMEZONE) -> datetime:
    for event in list_solar_terms_for_year(year, timezone_name):
        if event["name"] == term_name and event["at"].year == year:
            return event["at"]
    raise ValueError(f"solar term not found: year={year}, term={term_name}")
