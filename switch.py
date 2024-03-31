from homeassistant.components.switch import SwitchEntity
from homeassistant.const import CONF_NAME

DOMAIN = 'hello_state'


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    device_name = config.get(CONF_NAME)
    device_switch = MyDeviceSwitch(device_name)
    async_add_entities([device_switch])


async def async_setup_entry(hass, config_entry, async_add_entities):
    device_name = hass.data[DOMAIN].get(CONF_NAME)
    device_switch = MyDeviceSwitch(device_name)
    async_add_entities([device_switch])
    return True


class MyDeviceSwitch(SwitchEntity):
    def __init__(self, name):
        """Initialize the switch."""
        self.entity_id = f"switch.{name}"
        self._name = name
        self._state = False

    @property
    def name(self):
        """Return the display name of this switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    async def async_turn_on(self, **kwargs):
        """Turn on the switch."""
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        """Turn off the switch."""
        self._state = False
        self.async_write_ha_state()

    @property
    def device_info(self):
        """Get Information about this device."""
        return {
            # Assuming "unique_id" from your device info variable is used for identifiers
            "identifiers": {(DOMAIN, self._name)},
        }
