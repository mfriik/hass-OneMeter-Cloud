import logging
import aiohttp
import async_timeout
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, CoordinatorEntity
from homeassistant.components.sensor import SensorEntity
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.const import UnitOfEnergy, PERCENTAGE
from homeassistant.util import slugify

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback) -> None:
    session = aiohttp.ClientSession()
    api_key = entry.data["api_key"]
    device_id = entry.data["device_id"]
    device_name = entry.data["device_name"]
    scan_interval = timedelta(seconds=entry.data.get("scan_interval", 900))

    url = f"https://cloud.onemeter.com/api/devices/{device_id}"
    headers = {"Authorization": api_key}

    async def async_update_data():
        async with async_timeout.timeout(10):
            async with session.get(url, headers=headers) as response:
                data = await response.json()
                _LOGGER.debug("Received data from OneMeter API: %s", data)
                return data

    coordinator = DataUpdateCoordinator(
        hass,
        logger=_LOGGER,
        name=f"{device_name} Coordinator",
        update_method=async_update_data,
        update_interval=scan_interval,
    )

    await coordinator.async_config_entry_first_refresh()

    def last_refresh_fn(_: dict):
        return coordinator.last_update_success_time.isoformat() if coordinator.last_update_success_time else None

    sensors = [
        ("Firmware Version", lambda d: f"v.{d['firmware']['currentVersion']}", None, "mdi:chip"),
        ("Last Readout", lambda d: d["lastReading"]["date"], None, "mdi:clock-outline"),
        ("Battery Level", lambda d: d["lastReading"]["BATTERY_PC"], PERCENTAGE, "mdi:battery"),
        ("Total Consumption", lambda d: d["lastReading"]["OBIS"]["15_8_0"], UnitOfEnergy.KILO_WATT_HOUR, "mdi:lightning-bolt"),
        ("Current Month Consumption", lambda d: round(d["usage"]["thisMonth"], 2), UnitOfEnergy.KILO_WATT_HOUR, "mdi:calendar-month"),
        ("Previous Month Consumption", lambda d: round(d["usage"]["previousMonth"], 2), UnitOfEnergy.KILO_WATT_HOUR, "mdi:calendar-month-outline"),
        ("Last API Refresh", last_refresh_fn, None, "mdi:api")
    ]

    entities = []
    for idx, (suffix, fn, unit, icon) in enumerate(sensors):
        # Keep the original entity name for entity ID generation
        full_name = f"OneMeter_{device_name}_{suffix}"
        # Create friendly name in the format "{device_name} {sensor_name}"
        friendly_name = f"{device_name} {suffix}"
        entities.append(OneMeterSensor(coordinator, full_name, friendly_name, fn, unit, icon, idx, entry.entry_id))

    async_add_entities(entities)

    await create_utility_meter(hass, device_name, entry)

class OneMeterSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator, entity_name, friendly_name, fn, unit, icon, idx, config_entry_id):
        super().__init__(coordinator)
        self._entity_name = entity_name  # Used for entity ID generation
        self._friendly_name = friendly_name  # Used for display name
        self._value_fn = fn
        self._unit = unit
        self._icon = icon
        self._unique_id = f"{config_entry_id}_{idx}"
        self._attr_native_unit_of_measurement = unit
        self._attr_name = friendly_name  # This sets the friendly name
        self._attr_icon = icon  # This sets the icon
        self._attr_device_info = {
            "identifiers": {(DOMAIN, config_entry_id)},
            "name": entity_name.split('_')[1],  # Extract device name from entity_name
            "manufacturer": "OneMeter",
            "entry_type": "service",
        }

        if "Usage Level" in entity_name or "Consumption" in entity_name:
            self._attr_state_class = "total_increasing"
            self._attr_device_class = "energy"
        elif "Last API Refresh" in entity_name:
            self._attr_device_class = "timestamp"

    @property
    def name(self):
        # Return the entity name for entity ID generation
        return self._entity_name

    @property
    def unique_id(self):
        return self._unique_id

    @property
    def native_value(self):
        try:
            return self._value_fn(self.coordinator.data)
        except Exception as e:
            _LOGGER.warning("Error parsing value for %s: %s", self._friendly_name, e)
            return None

async def create_utility_meter(hass: HomeAssistant, device_name: str, entry: ConfigEntry):
    from homeassistant.helpers import entity_registry as er

    sensor_entity_id = f"sensor.onemeter_{slugify(device_name)}_usage_level"
    meter_name = f"OneMeter_{device_name}_UtilityMeter"
    meter_id = f"utility_meter.onemeter_{slugify(device_name)}_utilitymeter"

    registry = er.async_get(hass)
    if registry.async_get(meter_id):
        return

    data = {
        "name": meter_name,
        "source": sensor_entity_id,
        "cycle": "monthly",
        "unique_id": f"{entry.entry_id}_utility",
        "delta_values": False
    }

    await hass.config_entries.flow.async_init(
        "utility_meter",
        context={"source": "integration"},
        data=data
    )

    hass.components.persistent_notification.create(
        f"Utility meter '{meter_name}' was created. Add it to the Energy Dashboard under Grid Consumption.",
        title="OneMeter Setup",
        notification_id="onemeter_energy_dashboard",
    )