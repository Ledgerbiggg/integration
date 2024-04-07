

"""Demo light platform that implements lights."""

from __future__ import annotations

import random
from typing import Any

from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP,
    ATTR_EFFECT,
    ATTR_HS_COLOR,
    ATTR_RGBW_COLOR,
    ATTR_RGBWW_COLOR,
    ATTR_WHITE,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)
from homeassistant.helpers.device_registry import DeviceInfo
import random
from typing import Any

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.components.light import (
    ATTR_BRIGHTNESS,
    ATTR_COLOR_TEMP,
    ATTR_EFFECT,
    ATTR_HS_COLOR,
    ATTR_RGBW_COLOR,
    ATTR_RGBWW_COLOR,
    ATTR_WHITE,
    ColorMode,
    LightEntity,
    LightEntityFeature,
)

DOMAIN = "hello_state"

LIGHT_COLORS = [(56, 86), (345, 75)]

LIGHT_EFFECT_LIST = ["rainbow", "none"]

LIGHT_TEMPS = [240, 380]

SUPPORT_DEMO = {ColorMode.HS, ColorMode.COLOR_TEMP}
SUPPORT_DEMO_HS_WHITE = {ColorMode.HS, ColorMode.WHITE}


async def async_setup_entry(
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        async_add_entities: AddEntitiesCallback,
) -> None:
    async_add_entities(
        [
            HelloLight(
                available=True,
                state=True,
                unique_id="light_1",
                device_name="hello_light_1",
                effect_list=LIGHT_EFFECT_LIST,
                effect=LIGHT_EFFECT_LIST[0],
            ),
            HelloLight(
                available=True,
                state=True,
                unique_id="light_2",
                device_name="hello_light_2",
                ct=LIGHT_TEMPS[1],
            ),
            HelloLight(
                available=True,
                state=True,
                unique_id="light_3",
                device_name="hello_light_3",
                hs_color=LIGHT_COLORS[1],
            ),
            HelloLight(
                available=True,
                state=True,
                unique_id="light_4",
                device_name="hello_light_4",
                ct=LIGHT_TEMPS[1],
                rgbw_color=(255, 0, 0, 255),
                supported_color_modes={ColorMode.RGBW},
            ),
            HelloLight(
                available=True,
                state=True,
                unique_id="light_5",
                device_name="hello_light_5",
                rgbww_color=(255, 0, 0, 255, 0),
                supported_color_modes={ColorMode.RGBWW},
            ),
            HelloLight(
                available=True,
                state=True,
                unique_id="light_6",
                device_name="hello_light_6",
                hs_color=LIGHT_COLORS[1],
                supported_color_modes=SUPPORT_DEMO_HS_WHITE,
            ),

        ])

class HelloLight(LightEntity):
    """Representation of a demo light."""

    _attr_has_entity_name = True
    _attr_name = None
    _attr_should_poll = False

    def __init__(
            self,
            unique_id: str,
            device_name: str,
            state: bool,
            available: bool = False,
            brightness: int = 180,
            ct: int | None = None,
            effect_list: list[str] | None = None,
            effect: str | None = None,
            hs_color: tuple[int, int] | None = None,
            rgbw_color: tuple[int, int, int, int] | None = None,
            rgbww_color: tuple[int, int, int, int, int] | None = None,
            supported_color_modes: set[ColorMode] | None = None,
    ) -> None:
        """Initialize the light."""
        self._available = True
        self._brightness = brightness
        self._ct = ct or random.choice(LIGHT_TEMPS)
        self._effect = effect
        self._effect_list = effect_list
        self._hs_color = hs_color
        self._rgbw_color = rgbw_color
        self._rgbww_color = rgbww_color
        self._state = state
        self._unique_id = unique_id
        if hs_color:
            self._color_mode = ColorMode.HS
        elif rgbw_color:
            self._color_mode = ColorMode.RGBW
        elif rgbww_color:
            self._color_mode = ColorMode.RGBWW
        else:
            self._color_mode = ColorMode.COLOR_TEMP
        if not supported_color_modes:
            supported_color_modes = SUPPORT_DEMO
        self._color_modes = supported_color_modes
        if self._effect_list is not None:
            self._attr_supported_features |= LightEntityFeature.EFFECT
        self._attr_device_info = DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self.unique_id)
            },
            name=device_name,
        )

    @property
    def unique_id(self) -> str:
        """Return unique ID for light."""
        return self._unique_id

    @property
    def available(self) -> bool:
        """Return availability."""
        # This demo light is always available, but well-behaving components
        # should implement this to inform Home Assistant accordingly.
        return self._available

    @property
    def brightness(self) -> int:
        """Return the brightness of this light between 0..255."""
        return self._brightness

    @property
    def color_mode(self) -> str | None:
        """Return the color mode of the light."""
        return self._color_mode

    @property
    def hs_color(self) -> tuple[int, int] | None:
        """Return the hs color value."""
        return self._hs_color

    @property
    def rgbw_color(self) -> tuple[int, int, int, int] | None:
        """Return the rgbw color value."""
        return self._rgbw_color

    @property
    def rgbww_color(self) -> tuple[int, int, int, int, int] | None:
        """Return the rgbww color value."""
        return self._rgbww_color

    @property
    def color_temp(self) -> int:
        """Return the CT color temperature."""
        return self._ct

    @property
    def effect_list(self) -> list[str] | None:
        """Return the list of supported effects."""
        return self._effect_list

    @property
    def effect(self) -> str | None:
        """Return the current effect."""
        return self._effect

    @property
    def is_on(self) -> bool:
        """Return true if light is on."""
        return self._state

    @property
    def supported_color_modes(self) -> set[ColorMode]:
        """Flag supported color modes."""
        return self._color_modes

    async def async_turn_on(self, **kwargs: Any) -> None:
        """Turn the light on."""
        self._state = True

        if ATTR_BRIGHTNESS in kwargs:
            self._brightness = kwargs[ATTR_BRIGHTNESS]

        if ATTR_COLOR_TEMP in kwargs:
            self._color_mode = ColorMode.COLOR_TEMP
            self._ct = kwargs[ATTR_COLOR_TEMP]

        if ATTR_EFFECT in kwargs:
            self._effect = kwargs[ATTR_EFFECT]

        if ATTR_HS_COLOR in kwargs:
            self._color_mode = ColorMode.HS
            self._hs_color = kwargs[ATTR_HS_COLOR]

        if ATTR_RGBW_COLOR in kwargs:
            self._color_mode = ColorMode.RGBW
            self._rgbw_color = kwargs[ATTR_RGBW_COLOR]

        if ATTR_RGBWW_COLOR in kwargs:
            self._color_mode = ColorMode.RGBWW
            self._rgbww_color = kwargs[ATTR_RGBWW_COLOR]

        if ATTR_WHITE in kwargs:
            self._color_mode = ColorMode.WHITE
            self._brightness = kwargs[ATTR_WHITE]

        # As we have disabled polling, we need to inform
        # Home Assistant about updates in our state ourselves.
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs: Any) -> None:
        """Turn the light off."""
        self._state = False

        # As we have disabled polling, we need to inform
        # Home Assistant about updates in our state ourselves.
        self.async_write_ha_state()
