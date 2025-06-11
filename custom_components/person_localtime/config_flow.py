from homeassistant import config_entries
from homeassistant.core import callback
import voluptuous as vol

from homeassistant.helpers.selector import (
    EntitySelector,
    EntitySelectorConfig
)

from .const import DOMAIN


class PersonTimezoneConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Person Localtime."""

    VERSION = 1

    async def async_step_user(self, user_input=None):
        """Handle the initial step."""
        if user_input is not None:
            person_entity_id = user_input["person_entity_id"]

            # Try to fetch the friendly name from the entity state
            person_state = self.hass.states.get(person_entity_id)
            person_name = person_state.name if person_state else "Person"

            return self.async_create_entry(
                title=person_name,
                data={"person_entity_id": person_entity_id},
            )

        return self.async_show_form(
            step_id="user",
            data_schema=vol.Schema({
                vol.Required("person_entity_id"): EntitySelector(
                    EntitySelectorConfig(domain="person")
                )
            }),
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        return PersonTimezoneOptionsFlow(config_entry)


class PersonTimezoneOptionsFlow(config_entries.OptionsFlow):
    """Handle options for the integration."""

    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        """Manage the integration options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=vol.Schema({
                vol.Required(
                    "person_entity_id",
                    default=self.config_entry.data.get("person_entity_id")
                ): EntitySelector(EntitySelectorConfig(domain="person")),
            }),
        )

