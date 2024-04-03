from homeassistant import config_entries
from homeassistant.const import CONF_NAME
import voluptuous as vol

DOMAIN = "hello_state"
ROOMS = ["卧室", "厨房"]  # 列出所有可能的房间


# async def async_setup_entry(hass, entry):
#     """
#     这个函数是在你的集成被用户添加到 Home Assistant 后执行的。它的主要任务是设置集成，并初始化你的设备和服务。
#     :param hass:  这是一个指向当前 Home Assistant 运行实例的引用。
#     :param entry: 这是一个 ConfigEntry 对象，包含用户在设置集成时提供的数据（你在配置流程中收集的数据）。
#     :return:
#     """
#     hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "switch"))
#     return True


# 添加集成的时候提示词语
class HelloStateConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):

    # @staticmethod
    # @callback
    # def async_get_options_flow(
    #         config_entry: config_entries.ConfigEntry,
    # ) -> config_entries.OptionsFlow:
    #     """Create the options flow."""
    #     return OptionsFlowHandler(config_entry)

    async def async_step_user(self, user_input=None):
        if user_input is not None:
            await self.async_set_unique_id(user_input['name'])
            # 因为我们允许用户通过UI改变设备的名字，所以选择更新设备名
            self._abort_if_unique_id_configured(updates={CONF_NAME: user_input[CONF_NAME]})

            return self.async_create_entry(title=user_input[CONF_NAME], data=user_input)
        return await self._show_config_form()

        # 如果是用户第一次设置或者需要更改设置，会走这里

    async def _show_config_form(self, errors=None):
        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({vol.Required("name"): str}),
            errors=errors or {},
        )

# class OptionsFlowHandler(config_entries.OptionsFlow):
#     def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
#         """Initialize options flow."""
#         self.config_entry = config_entry
#
#     async def async_step_init(
#         self, user_input: dict[str, Any] | None = None
#     ) -> FlowResult:
#         """Manage the options."""
#         if user_input is not None:
#             return self.async_create_entry(title="", data=user_input)
#
#         return self.async_show_form(
#             step_id="init",
#             data_schema=vol.Schema(
#                 {
#                     vol.Required(
#                         "show_things",
#                         default=self.config_entry.options.get("show_things"),
#                     ): bool
#                 }
#             ),
#         )