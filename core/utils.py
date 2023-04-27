from django.utils.translation import gettext_lazy as _
from enum import Enum

class RoleCodename(Enum):
    ADMINISTRATOR = 'BI-RL-ADM'
    DOMAIN_MANAGER = 'BI-RL-DMA'
    ANALYST = 'BI-RL-ANA'
    VALIDATOR = 'BI-RL-VAL'
    AUDITOR = 'BI-RL-AUD'

    def __str__(self) -> str:
        return self.value

class UserGroupCodename(Enum):
    ADMINISTRATOR = 'BI-UG-ADM'
    GLOBAL_AUDITOR = 'BI-UG-GAD'
    GLOBAL_VALIDATOR = 'BI-UG-GVA'
    DOMAIN_MANAGER = 'BI-UG-DMA'
    ANALYST = 'BI-UG-ANA'
    VALIDATOR = 'BI-UG-VAL'
    AUDITOR = 'BI-UG-AUD'

    def __str__(self) -> str:
        return self.value

BUILTIN_ROLE_CODENAMES = {
    str(RoleCodename.ADMINISTRATOR): _('Administrator'),
    str(RoleCodename.DOMAIN_MANAGER): _('Domain manager'),
    str(RoleCodename.ANALYST): _('Analyst'),
    str(RoleCodename.VALIDATOR): _('Validator'),
    str(RoleCodename.AUDITOR): _('Auditor'),
}

BUILTIN_USERGROUP_CODENAMES = {
    str(UserGroupCodename.ADMINISTRATOR): _('Administrator'),
    str(UserGroupCodename.GLOBAL_AUDITOR): _('Auditor'),
    str(UserGroupCodename.GLOBAL_VALIDATOR): _('Validator'),
    str(UserGroupCodename.DOMAIN_MANAGER): _('Domain manager'),
    str(UserGroupCodename.ANALYST): _('Analyst'),
    str(UserGroupCodename.VALIDATOR): _('Validator'),
    str(UserGroupCodename.AUDITOR): _('Auditor'),
}

COUNTRY_FLAGS = {
    'fr': '🇫🇷',
    'en': '🇬🇧',
}

LANGUAGES = {
    'fr': _('French'),
    'en': _('English'),
}