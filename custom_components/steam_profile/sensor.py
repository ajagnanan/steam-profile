"""Sensor for Steam account status."""
from __future__ import annotations

from datetime import datetime
from time import localtime, mktime
from typing import cast

from homeassistant.components.sensor import SensorEntity, SensorEntityDescription
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.typing import StateType
from homeassistant.util.dt import utc_from_timestamp

from .const import (
    CONF_ACCOUNTS,
    DOMAIN,
    LOGGER,
    STEAM_API_URL,
    STEAM_HEADER_IMAGE_FILE,
    STEAM_ICON_URL,
    STEAM_MAIN_IMAGE_FILE,
    STEAM_STATUSES,
    STEAM_JOIN_LOBBY_URL_FORMAT
)
from .coordinator import SteamProfileDataUpdateCoordinator
from .entity import SteamProfileEntity

PARALLEL_UPDATES = 1

async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up the Steam platform."""
    async_add_entities(
        SteamProfileSensor(hass.data[DOMAIN][entry.entry_id], account)
        for account in entry.options[CONF_ACCOUNTS]
    )
    async_add_entities(
        SteamLobbySensor(hass.data[DOMAIN][entry.entry_id], account)
        for account in entry.options[CONF_ACCOUNTS]
    )

class SteamProfileSensor(SteamProfileEntity, SensorEntity):
    """A class for the Steam Profile."""

    def __init__(self, coordinator: SteamProfileDataUpdateCoordinator, account: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = SensorEntityDescription(
            key=account,
            name=account,
            icon="mdi:steam",
        )
        self._attr_unique_id = f"sensor.steam_profile_{account}"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if self.entity_description.key in self.coordinator.data:
            player = self.coordinator.data[self.entity_description.key]
            return STEAM_STATUSES[cast(int, player["personastate"])]
        return None

    @property
    def extra_state_attributes(self) -> dict[str, str | int | datetime]:
        """Return the state attributes of the sensor."""
        if self.entity_description.key not in self.coordinator.data:
            return {}
        player = self.coordinator.data[self.entity_description.key]

        attrs: dict[str, str | int | datetime] = {}
        if game := player.get("gameextrainfo"):
            attrs["game"] = game
        if game_id := player.get("gameid"):
            attrs["game_id"] = game_id
            game_url = f"{STEAM_API_URL}{player['gameid']}/"
            attrs["game_image_header"] = f"{game_url}{STEAM_HEADER_IMAGE_FILE}"
            attrs["game_image_main"] = f"{game_url}{STEAM_MAIN_IMAGE_FILE}"
            if info := self._get_game_icon(player):
                attrs["game_icon"] = f"{STEAM_ICON_URL}{game_id}/{info}.jpg"
        self._attr_name = str(player["personaname"]) or None
        self._attr_entity_picture = str(player["avatarmedium"]) or None
        if last_online := cast(int | None, player.get("lastlogoff")):
            attrs["last_online"] = utc_from_timestamp(mktime(localtime(last_online)))
        if level := self.coordinator.data[self.entity_description.key]["level"]:
            attrs["level"] = level
        return attrs

    def _get_game_icon(self, player: dict) -> str | None:
        """Get game icon identifier."""
        game_icons = self.coordinator.data[self.entity_description.key]["game_icons"]
        return game_icons[int(player.get("gameid"))]

class SteamLobbySensor(SteamProfileEntity, SensorEntity):
    """A class for the Steam lobby."""

    def __init__(self, coordinator: SteamProfileDataUpdateCoordinator, account: str) -> None:
        """Initialize the sensor."""
        super().__init__(coordinator)
        self.entity_description = SensorEntityDescription(
            key=account,
            name="Lobby",
            icon="mdi:gamepad-variant",
        )
        self._attr_unique_id = f"sensor.steam_lobby_{account}"

    @property
    def native_value(self) -> StateType:
        """Return the state of the sensor."""
        if self.entity_description.key not in self.coordinator.data:
            return None
        player = self.coordinator.data[self.entity_description.key]

        if lobby_steam_id := player.get("lobbysteamid"):
            game_id = player.get("gameid")
            return STEAM_JOIN_LOBBY_URL_FORMAT.format(
                game_id=game_id,
                lobby_steam_id=lobby_steam_id,
                account=self.entity_description.key
            )
        else:
            return None

    @property
    def extra_state_attributes(self) -> dict[str, str | int | datetime]:
        """Return the state attributes of the sensor."""
        if self.entity_description.key not in self.coordinator.data:
            return {}
        player = self.coordinator.data[self.entity_description.key]

        attrs: dict[str, str | int | datetime] = {}
        if lobby_steam_id := player.get("lobbysteamid"):
            game_id = player.get("gameid")
            game_extra_info = player.get("gameextrainfo")

            attrs["steam_id"] = self.entity_description.key
            attrs["game_id"] = game_id
            attrs["game_extra_info"] = game_extra_info
            attrs["lobby_steam_id"] = lobby_steam_id
            if info := self._get_game_icon(player):
                game_icon = f"{STEAM_ICON_URL}{game_id}/{info}.jpg"
                attrs["game_icon"] = game_icon
                self._attr_name = str(game_extra_info) or None
                self._attr_entity_picture = str(game_icon) or None

        return attrs
    
    def _get_game_icon(self, player: dict) -> str | None:
        """Get game icon identifier."""
        game_icons = self.coordinator.data[self.entity_description.key]["game_icons"]
        return game_icons[int(player.get("gameid"))]
