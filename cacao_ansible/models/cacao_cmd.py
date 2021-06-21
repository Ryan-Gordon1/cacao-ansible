from pydantic import BaseModel, ValidationError, validator
from typing import Literal
from models import AnsibleCmdSpec


class CACAOCmd(BaseModel):
    """CACAOCmd: The CACAO command object (command-data) contains detailed information about the commands that
        are to be executed or processed automatically or manually as part of a workflow step (see section 4).
        Each command listed in a step may be of a different command type, however, all commands listed in a
        single step MUST be processed or executed by all of the targets defined in that step.
        Commands can use and refer to variables just like other parts of the playbook. For each command either
        the command property or the command_b64 property MUST be present.
        The individual commands MAY be defined in other specifications, and when possible will be mapped to
        the JSON structure of this specification. When that is not possible, they will be base64 encoded
        Source: http://docs.oasis-open.org/cacao/security-playbooks/v1.0/security-playbooks-v1.0.pdf
    """
    type: Literal['manual', 'http-api', 'bash', 'ssh',
                  'openc2-json', 'ansible-json', 'attack-cmd']
    command: str

    @validator('command')
    def validate_command(cls, v, values, **kwargs):
        if 'type' in values and values['type'] == "ansible-json":
            try:
                AnsibleCmdSpec(
                    **kwargs
                )
            except ValidationError as e:
                raise ValueError(
                    'Command type was provided as %s but command did not conform to the spec. Error raised: %s', values['type'], e)
        return v
