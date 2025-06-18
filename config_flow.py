import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN

DEFAULT_SCAN_INTERVAL = 300

class OneMeterConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        if user_input is not None:
            return self.async_create_entry(
                title=user_input["device_name"],
                data=user_input
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("api_key"): str,
                vol.Required("device_id"): str,
                vol.Required("device_name"): str,
                vol.Optional("scan_interval", default=DEFAULT_SCAN_INTERVAL): vol.All(int, vol.Clamp(min=60, max=86400)),
            }),
        )
