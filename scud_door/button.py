
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
        self._attr_name = f"Открыть {door['name']}"
        self._attr_unique_id = f"scud_door_{door['id']}"
        self.door_id = door['id']

    async def async_press(self):
        await self.coordinator.open_door(self.door_id)
