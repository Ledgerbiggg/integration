import logging

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .light import MyLight

DOMAIN = "hello_state"
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass: HomeAssistant, hass_config):
    # 添加开关
    hass.helpers.discovery.load_platform('switch', DOMAIN, {}, hass_config)

    # 添加服务
    async def handle_my_service(call):
        # Get the service data
        url = call.data.get('url',
                            'http://192.168.140.58:8000/user')
        username = call.data.get('username', 'ledger')
        # 添加参数
        params = {'username': username}
        # 获取一个http请求的客户端
        session = async_get_clientsession(hass)
        async with session.get(url, params=params) as response:
            response_text = response.text()
            _LOGGER.info(response_text)

    hass.services.async_register(DOMAIN, 'my_service', handle_my_service)

    # 添加设备
    my_light = MyLight()
    hass.data.setdefault("hello_state", []).append(my_light)
    # 将设备绑定到集成上面
    hass.helpers.discovery.load_platform("light", "hello_state", {}, hass_config)

    return True


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry):
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "light"))
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "switch"))
    return True


# async def async_update_options(hass: HomeAssistant, entry: ConfigEntry):
#     return
#
#
# async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry):
#     return
#
#
# async def async_add_setuper(hass: HomeAssistant, config, domain, setuper):
#     return
