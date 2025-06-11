"""Constants for the Person Localtime integration."""

# Domain of the integration
DOMAIN = "person_localtime"

# Sensor type keys
SENSOR_TIMEZONE = "timezone"
SENSOR_LOCAL_TIME = "local_time"
SENSOR_SUN_POSITION = "sun_position"

# Sensor type definitions: [Name, Icon, Unit (unused but reserved)]
SENSOR_TYPES = {
    SENSOR_TIMEZONE: ["Timezone", "mdi:earth", ""],
    SENSOR_LOCAL_TIME: ["Local Time", "mdi:clock-outline", ""],
    SENSOR_SUN_POSITION: ["Sun Position", "mdi:white-balance-sunny", ""],
}

