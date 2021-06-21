from typing import Optional
from pydantic import BaseModel, validator

from uuid import UUID

class AnsibleCmdSpec(BaseModel):
    """AnsibleCmdSpec is a definition of parameters
    needed for the ansible-json command to be considered valid.
    The spec supports both the running of modules and playbooks
    """
    name: str = "ansible-json"
    id: UUID
    private_data_dir: Optional[str]
    artifact_dir: Optional[str]
    is_module: bool = False
    module_name: Optional[str]
    module_args: Optional[str]
    module_hosts: Optional[str]
    playbook_name: str
    playbook_args: dict

    @validator('module_name')
    def check_module_name(cls, v, values, **kwargs):
        if 'is_module' in values and values['is_module'] and not v:
            raise ValueError(
                'module_name need to be provided when is_module is true')
        return v

    @validator('module_args')
    def check_module_args(cls, v, values, **kwargs):
        if 'is_module' in values and values['is_module'] and not v:
            raise ValueError(
                'module_args need to be provided when is_module is true')
        return v
