import logging
from .switch import MyDeviceSwitch
from homeassistant.helpers.entity_platform import async_get_platforms
from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.aiohttp_client import async_get_clientsession

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

    # # 添加设备
    # my_light = MyLight()
    # hass.data.setdefault("hello_state", []).append(my_light)
    # async_add_entities([my_light], update_before_add=True)
    # 将设备绑定到集成上面

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

    # 在这里你可以创建和存储设备实例，它可以是一个智能开关、传感器或任何其他设备
    # device = MyDeviceSwitch(entry.data['name'])

    # 创建并初始化开关实体
    # async def async_add_device_entities():
    #     """添加和注册这个设备相关的实体。"""
    #     # 获取开关平台
    #     platform = await async_get_platforms(hass, DOMAIN)
    #     sender = util.RequestSender()
    #     sender.send_request()
    #
    #     # 创建开关实体。这应该是你在switch模块定义的实体类
    #     my_switch_entity = MyDeviceSwitch("newSwitch")
    #
    #     # 如果你的实体还有其它的设置，可以在此处配置
    #
    #     # 添加实体
    #     if platform:
    #         platform[0].async_add_entities([my_switch_entity])
    #
    # hass.async_create_task(async_add_device_entities())

    return True
