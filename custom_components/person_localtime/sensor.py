import logging
from datetime import datetime, timedelta
import pytz
from astral.sun import sun
from astral import LocationInfo
from timezonefinder import TimezoneFinder

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_LATITUDE, ATTR_LONGITUDE
from homeassistant.helpers.entity import Entity
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from typing import Any

from .const import (
    DOMAIN,
    SENSOR_TYPES,
    SENSOR_TIMEZONE,
    SENSOR_LOCAL_TIME,
    SENSOR_SUN_POSITION
)

import asyncio

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback
) -> None:
    """Set up Person Localtime sensors from a config entry."""
    _LOGGER.debug("Setting up Person Localtime sensors for entry: %s", entry)

    async def update_method() -> dict[str, Any]:
        return await async_update_data(hass, entry)

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        name="person_localtime",
        update_method=update_method,
        update_interval=timedelta(seconds=30),
    )

    await coordinator.async_refresh()

    sensors = [
        PersonLocaltimeSensor(coordinator, sensor_type, entry)
        for sensor_type in SENSOR_TYPES
    ]
    async_add_entities(sensors, True)


async def async_update_data(hass: HomeAssistant, entry: ConfigEntry) -> dict[str, Any]:
    """Fetch data from the person entity and compute local sun information."""
    entity_id = entry.data["person_entity_id"]
    _LOGGER.debug("Updating data for entity: %s", entity_id)

    person_state = hass.states.get(entity_id)
    if not person_state:
        _LOGGER.warning("Person entity %s not found", entity_id)
        return _default_data()

    latitude = person_state.attributes.get(ATTR_LATITUDE)
    longitude = person_state.attributes.get(ATTR_LONGITUDE)
    _LOGGER.debug("Location - Latitude: %s, Longitude: %s", latitude, longitude)

    if latitude is None or longitude is None:
        _LOGGER.warning("Location for %s not available", entity_id)
        return _default_data()

    timezone_str = await asyncio.to_thread(resolve_timezone, latitude, longitude)
    if not timezone_str:
        _LOGGER.warning("Timezone not found for %s", entity_id)
        return _default_data()

    timezone = pytz.timezone(timezone_str)
    now = datetime.now(timezone)
    location = LocationInfo("", "", timezone_str, latitude, longitude)
    s = sun(location.observer, date=now, tzinfo=timezone)

    return {
        SENSOR_LOCAL_TIME: now.strftime('%H:%M'),
        SENSOR_TIMEZONE: timezone_str,
        SENSOR_SUN_POSITION: "Above" if s["sunrise"] <= now <= s["sunset"] else "Below",
        "sunrise": s["sunrise"].strftime('%H:%M:%S %z'),
        "sunset": s["sunset"].strftime('%H:%M:%S %z'),
    }


def resolve_timezone(latitude: float, longitude: float) -> str:
    """Resolve the timezone for the given latitude and longitude."""
    return TimezoneFinder().timezone_at(lat=latitude, lng=longitude)


def _default_data() -> dict[str, str]:
    """Return default placeholder data when information is unavailable."""
    return {
        SENSOR_LOCAL_TIME: "Unknown",
        SENSOR_TIMEZONE: "Unknown",
        SENSOR_SUN_POSITION: "Unknown",
        "sunrise": "Unknown",
        "sunset": "Unknown",
    }


class PersonLocaltimeSensor(CoordinatorEntity, Entity):
    """Representation of a Person Localtime Sensor."""

    def __init__(self, coordinator, sensor_type: str, entry: ConfigEntry) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.sensor_type = sensor_type
        self.entry = entry
        self._attr_name = f"{entry.title} {SENSOR_TYPES[sensor_type][0]}"
        self._attr_icon = SENSOR_TYPES[sensor_type][1]
        self._attr_unique_id = f"{entry.entry_id}_{sensor_type}"
        _LOGGER.debug(f"Initialized sensor: {self._attr_name}")

    @property
    def state(self) -> str:
        """Return the state of the sensor."""
        return self.coordinator.data.get(self.sensor_type, "Unknown")

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return additional attributes for sun position sensor."""
        if self.sensor_type == SENSOR_SUN_POSITION:
            return {
                "sunrise": self.coordinator.data.get("sunrise", "Unknown"),
                "sunset": self.coordinator.data.get("sunset", "Unknown"),
            }
        return {}

    @property
    def device_info(self) -> dict[str, Any]:
        """Return device information."""
        return {
            "identifiers": {(DOMAIN, self.entry.entry_id)},
            "name": self.entry.title,
            "manufacturer": "Custom Integration",
        }

