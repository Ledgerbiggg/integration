import logging

from homeassistant.helpers.aiohttp_client import async_get_clientsession

DOMAIN = "hello_state"
_LOGGER = logging.getLogger(__name__)


async def async_setup(hass, config):

    # Return boolean to indicate that initialization was successful.
    async def handle_my_service(call):
        session = async_get_clientsession(hass)
        async with session.get('http://192.168.140.58:8000/user') as response:
            response_text = await response.text()  # 这里可以处理你的响应内容，比如解析、打印或保存数据等
            _LOGGER.info(response_text)

    async def handle_my_service2(call):
        # Get the service data
        url = call.data.get('url',
                            'http://192.168.140.58:8000/user')  # Use a default value in case 'url' is not provided
        session = async_get_clientsession(hass)
        async with session.get(url) as response:
            response_text = await response.text()
            _LOGGER.info(response_text)

    hass.states.set("hello_state.world", "closed")
    hass.helpers.discovery.load_platform('switch', DOMAIN, {}, config)
    hass.services.async_register(DOMAIN, 'my_service', handle_my_service)
    hass.services.async_register(DOMAIN, 'my_service2', handle_my_service)

    return True

