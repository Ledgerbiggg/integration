from homeassistant import config_entries
from homeassistant.const import CONF_NAME
import voluptuous as vol

DOMAIN = "hello_state"
ROOMS = ["卧室", "厨房"]  # 列出所有可能的房间


async def async_setup_entry(hass, entry):
    hass.async_create_task(hass.config_entries.async_forward_entry_setup(entry, "switch"))
    return True


# 添加集成的时候提示词语
class HelloStateConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
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
