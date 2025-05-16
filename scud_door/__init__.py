from .const import DOMAIN
from .coordinator import SCUDCoordinator

async def async_setup_entry(hass, entry):
    # Инициализируем словарь для данных интеграции, если ещё не создан
    if DOMAIN not in hass.data:
        hass.data[DOMAIN] = {}

    # Сохраняем экземпляр координатора в hass.data по entry_id
    coordinator = SCUDCoordinator(hass, entry.data)
    await coordinator.async_config_entry_first_refresh()
    hass.data[DOMAIN][entry.entry_id] = coordinator

    # Вместо устаревшего async_create_task await async_forward_entry_setups
    await hass.config_entries.async_forward_entry_setups(entry, ["button"])

    return True

async def async_unload_entry(hass, entry):
    # Удаляем координатор из hass.data
    unload_ok = await hass.config_entries.async_forward_entry_unload(entry, ["button"])
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
