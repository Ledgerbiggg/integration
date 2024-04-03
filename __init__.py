import logging
from .switch import MyDeviceSwitch
from homeassistant.helpers.entity_platform import async_get_platforms
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers import config_validation as cv, entity_platform
import voluptuous as vol

from .light import MyLight

DOMAIN = "hello_state"
_LOGGER = logging.getLogger(__name__)

async def async_setup(hass: HomeAssistant, hass_config):
    """
    这个函数是所有HomeAssistant集成的初始化函数，在HomeAssistant启动或重新加载配置时调用。
    函数执行一次。
    :param hass: HomeAssistant的实例，提供了与HomeAssistant系统进行交互的函数和属性。
    :param hass_config:  HomeAssistant的配置信息，包含了所有配置文件中的数据。
    :return: 初始化成功则返回True，否则返回False
    """

    # 添加服务
    async def handle_my_service(call):
        # 服务需要传入参数
        url = call.data.get('url',
                            'http://192.168.31.55:8000')
        username = call.data.get('username', 'ledger')
        # 添加参数
        params = {'username': username}
        # 获取一个http请求的客户端
        session = async_get_clientsession(hass)
        async with session.get(url, params=params) as response:
            response_text = response.text()
            _LOGGER.info(response_text)

    # 添加开关
    hass.helpers.discovery.load_platform('switch', "hello_state", {}, hass_config)
    # 添加服务
    hass.services.async_register(DOMAIN, 'my_service', handle_my_service)
    # 添加灯光
    hass.helpers.discovery.load_platform("light", "hello_state", {}, hass_config)
    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    """
    这个函数在添加或更新每一个集成的配置入口时被调用。
    对于每一个配置入口，函数将执行一次。
    :param hass: HomeAssistant的实例，提供了与HomeAssistant系统进行交互的函数和属性。
    :param entry: 代表单个集成的配置入口, 包含集成的配置数据。
    :return: 如果配置入口成功地设置了集成,则返回True, 否则返回False.
    """
    """设置设备和实体"""

    """Set up a configuration entry for your custom integration."""
    # Your custom setup code, if any

    hass.async_create_task(
        hass.config_entries.async_forward_entry_setup(entry, "switch")
    )

    return True
