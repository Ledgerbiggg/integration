from homeassistant.components.light import LightEntity
from homeassistant.const import CONF_NAME


async def async_setup_entry(hass, config_entry, async_add_entities):
    name = config_entry.data[CONF_NAME]
    new_light = MyLight(name)
    async_add_entities([new_light])


# 在你的 hello_state/light.py 文件中
async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Setup the hello_state Light platform."""
    # MyLight 类应该在这个文件中定义，或者从其它地方 import
    # create a new MyLight instance
    # 这应该与你实例化 MyLight 的方式一致
    new_light = MyLight()
    async_add_entities([new_light])


class MyLight(LightEntity):
    def __init__(self):
        self._state = False

    @property
    def name(self):
        return "my_light_hhh"

    @property
    def is_on(self):
        return self._state

    async def async_turn_on(self, **kwargs):
        self._state = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs):
        self._state = False
        self.async_write_ha_state()
