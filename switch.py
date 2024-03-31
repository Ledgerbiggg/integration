from homeassistant.components.switch import SwitchEntity


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    # hass.states.set("hello_state.world", "closed")
    async_add_entities([HelloSwitch(hass, "my_switch")])


class HelloSwitch(SwitchEntity):
    """Representation of a Hello Switch."""

    def __init__(self, hass, name):
        """Initialize the Hello switch."""
        self._state = False
        self.hass = hass
        self._name = name

    @property
    def name(self):
        """Return the display name of this switch."""
        return self._name

    @property
    def is_on(self):
        """Return true if switch is on."""
        return self._state

    async def turn_on(self, **kwargs):
        """Instruct the switch to turn on asynchronously."""
        self._state = True
        self.hass.states.set('hello_state.Hello_World', 'Works!')
        self.schedule_update_ha_state()

    async def turn_off(self, **kwargs):
        """Instruct the switch to turn off asynchronously."""
        self._state = False
        self.hass.states.set('hello_state.Hello_World', 'Closed')
        self.schedule_update_ha_state()

    async def update(self):
        """Fetch new state data for this Switch."""
        self._state = self.is_on