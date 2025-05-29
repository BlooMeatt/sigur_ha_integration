
import voluptuous as vol
from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from .const import DOMAIN

class SCUDConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="SIGUR HA Integration", data=user_input)

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("host"): str,
                vol.Required("port", default=3312): int,
                vol.Required("username"): str,
                vol.Required("password"): str,
            })
        )
