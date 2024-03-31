import logging

from homeassistant.helpers.aiohttp_client import async_get_clientsession

DOMAIN = "hello_state"
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):
    # 创建一个需要参数的服务(url)
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

    hass.helpers.discovery.load_platform('switch', DOMAIN, {}, config)
    hass.services.async_register(DOMAIN, 'my_service', handle_my_service)

    return True
