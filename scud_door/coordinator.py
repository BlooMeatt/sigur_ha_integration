
from datetime import timedelta
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.core import HomeAssistant
from .scud import SCUDClient
from .const import SCAN_INTERVAL
import logging

_LOGGER = logging.getLogger(__name__)


class SCUDCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, config):
        self.client = SCUDClient(**config)
        super().__init__(
            hass,
            _LOGGER,
            name="SCUD Door Coordinator",
            update_interval=timedelta(seconds=SCAN_INTERVAL),
        )

    async def _async_update_data(self):
        await self.client.connect()
        door_ids = await self.client.get_aplist()
        doors = []
        for door_id in door_ids:
            info = await self.client.get_apinfo(door_id)
            doors.append(info)
        return doors

    async def open_door(self, door_id):
        await self.client.open_door(door_id)
