import logging
import uuid
from typing import Any, Optional, Tuple
from pyhap.characteristic import Characteristic
from homeassistant.components.homekit.type_security_systems import (
    HK_ALARM_STAY_ARMED,
    HK_ALARM_AWAY_ARMED,
)

_LOGGER = logging.getLogger(__name__)

HAP_UUID_SECURITY_SYSTEM_CURRENT_STATE = uuid.UUID("{00000066-0000-1000-8000-0026BB765291}")
HAP_UUID_SECURITY_SYSTEM_TARGET_STATE = uuid.UUID("{00000067-0000-1000-8000-0026BB765291}")

_orig_client_update_value = Characteristic.client_update_value

def _patched_client_update_value(self, value: Any, sender_client_addr: Optional[Tuple[str, int]] = None):
    if (self.type_id == HAP_UUID_SECURITY_SYSTEM_CURRENT_STATE or self.type_id == HAP_UUID_SECURITY_SYSTEM_TARGET_STATE) and value == HK_ALARM_STAY_ARMED:
        value = HK_ALARM_AWAY_ARMED
    return _orig_client_update_value(self, value, sender_client_addr)

Characteristic.client_update_value = _patched_client_update_value

async def async_setup(hass, config):
    _LOGGER.info("hk_securitysystem_patch: loaded OK")
    return True
