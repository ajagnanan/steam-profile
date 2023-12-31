"""Entity classes for the Steam integration."""
from homeassistant.helpers.device_registry import DeviceEntryType
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DEFAULT_NAME, DOMAIN
from .coordinator import SteamProfileDataUpdateCoordinator

class SteamProfileEntity(CoordinatorEntity[SteamProfileDataUpdateCoordinator]):
    """Representation of a Steam Profile entity."""

    _attr_attribution = "Data provided by Steam"

    def __init__(self, coordinator: SteamProfileDataUpdateCoordinator) -> None:
        """Initialize a Steam entity."""
        super().__init__(coordinator)
        self._attr_device_info = DeviceInfo(
            configuration_url="https://store.steampowered.com",
            entry_type=DeviceEntryType.SERVICE,
            identifiers={(DOMAIN, coordinator.config_entry.entry_id)},
            manufacturer=DEFAULT_NAME,
            name=DEFAULT_NAME,
        )
