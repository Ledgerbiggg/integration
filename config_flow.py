from homeassistant import config_entries
from homeassistant.const import CONF_NAME
import voluptuous as vol

DOMAIN = "hello_state"
ROOMS = ["卧室", "厨房"]  # 列出所有可能的房间

# 添加集成的时候提示词语
class HelloStateConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            # Do whatever you need with user_input
            selected_room = user_input[CONF_NAME]
            # 判断是否为有效的房间
            if selected_room not in ROOMS:
                errors["base"] = "invalid_room"
            else:
                return self.async_create_entry(title="Hello State", data=user_input)

        data_schema = vol.Schema(
            {
                vol.Required(CONF_NAME): vol.In(ROOMS),
            }
        )

        return self.async_show_form(step_id="user", data_schema=data_schema, errors=errors)

    async def async_step_import(self, import_info):
        # this handles setup through YAML (if supported)
        return await self.async_step_user(import_info)
