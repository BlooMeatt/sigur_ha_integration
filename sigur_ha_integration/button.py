from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from .const import DOMAIN

async def async_setup_entry(hass, config_entry, async_add_entities):
    coordinator = hass.data[DOMAIN][config_entry.entry_id]
    entities = []

    for door in coordinator.data:
        entities.append(SCUDDoorButton(coordinator, door))

    async_add_entities(entities)


class SCUDDoorButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, door):
        super().__init__(coordinator)
        self.door_id = door['id']
        self.door_name = door['name']

        self._attr_name = "Открыть"
        self._attr_unique_id = f"sigur_door_{self.door_id}"

    async def async_press(self):
        await self.coordinator.open_door(self.door_id)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, f"door_{self.door_id}")},
            "name": self.door_name,
            "manufacturer": "SIGUR",
            "model": "СКУД TCP",
            "entry_type": "service",
        }
