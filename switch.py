import logging

from homeassistant.components.switch import SwitchEntity
from homeassistant.const import CONF_NAME

DOMAIN = 'hello_state'

_LOGGER = logging.getLogger(__name__)


# 编写一个开关
async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """
    这个函数在 Home Assistant 平台初始化时调用。比如当 Home Assistant 启动或者设备发现发生时，这个函数会被触发来设置平台。
    :param hass: 这是一个指向当前 Home Assistant 核心对象的引用。
    :param config: 这是一个字典，含有平台的配置信息。它通常来源于 `configuration.yaml` 文件。
    :param async_add_entities: 这个方法可以将新创建的或者已存在的设备实体添加到 Home Assistant 中。
    :param discovery_info:  这个是当设备用设备发现方式加入时提供的信息。通常包含一些设备特定的数据。
    """
    # device_name = config.get(CONF_NAME)
    device_switch = MyDeviceSwitch("my_switchinit")
    async_add_entities([device_switch])


async def async_setup_entry(hass, config_entry, async_add_entities):
    """
    这个函数在用户通过界面配置并添加集成后被调用。一旦集成成功初始化，就会触发此函数。
    :param hass: 这是一个指向当前 Home Assistant 核心对象的引用。
    :param config_entry: 这个对象包含了用户通过界面为集成做的配置信息。
    :param async_add_entities:  这个方法可以将新创建的或者已存在的设备实体添加到 Home Assistant 中。
    """
    # device_name = hass.data[DOMAIN].get(CONF_NAME)
    # device_name = "测试设备"
    # device_switch = MyDeviceSwitch("my_switch")
    # async_add_entities([device_switch])
    # _LOGGER.info('设备 %s 已成功添加到 Home Assistant', "my_switch")
    async_add_entities([MyDeviceSwitch("newSwitch222")], True)
    return True


class MyDeviceSwitch(SwitchEntity):
    added = False
    # _attr_should_poll = False
    def __init__(self, name):
        """Initialize the switch."""
        self.entity_id = f"switch.{name}"
        self._name = name
        self._state = False

    # async def async_added_to_hass(self):
    #     self.added = True
    #     await super().async_added_to_hass()
    #     await self.update_from_client()

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
