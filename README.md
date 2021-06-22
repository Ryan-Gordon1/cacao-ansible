# cacao-ansible
A tool which exposes functionality for 'ansible-json' as a command type within a CACAO Playbook. Eventually will be an CLI for running CACAO Playbooks.
## Overview 

There were 3 simple goals for this project which can be seen as milestones, these are:
+ Definition of the `ansible-json` command type which adheres to the CACAO Standard.
+ A cli tool which wraps Ansible Runner and runs either a playbook or module based on passed info
+ A full cli experience for running CACAO Playbooks, pass a playbook with `ansible-json` commands and run through the play

The first of the 3 goals is achieved with this repo. We have loosely defined a spec for ansible and this represents a natural splitting point so that the other goals can be achieved. 
A runner is provided which can be used to run a playbook. 

In another project I will define a cli tool and a UI experience for not just running `ansible-json` commands but a full CACAO playbook containing these commands.

## Specification 
In this repository we made an in-code specification definition of the `ansible-json` command using [pydantic](). This provides a quick method of validating your `ansible-json` command adheres to the specification defined below. This spec is a work in progress and will evolve over time.

```python
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
```

## Usage
In its current state this package is usable within another python package for either:
+ The running of ansible objects (playbooks or modules)
+ The validation of a AnsibleCacao command

The spec has optional params to allow you to provide either a playbook's parameters for execution or to provide parameters to directly run a module. 

## Installation
You can choose to install this package from Pypi which will grab the last released version: 
```
pip install cacao-ansible
```
..Or you can install this package directly from the source code:
```
python setup.py install
```


### What is CACAO? 
CACAO is a specification standard cultivated by OASIS. This specification defines the schema and taxonomy for collaborative automated course of action operations (CACAO) security playbooks and how these playbooks can be created, documented, and shared in a structured and standardized way across organizational boundaries and technological solutions. [source](https://docs.google.com/document/d/144kgoCnZbxc0CXms3EeACf4Sz84lmEt88JoVr4FnmSc/edit#)

### What is Ansible?
Ansible is a radically simple IT automation engine that automates cloud provisioning, configuration management, application deployment, intra-service orchestration, and many other IT needs.[-Source](https://www.ansible.com/overview/how-ansible-works)

Most importantly to this project and the CACAO standard is Ansible defines a form of Security Language for the above mentioned automation operations and through this project a CACAO playbook should be able to leverage the entire security community on [Ansible Galaxy](https://galaxy.ansible.com/)

### Use Case Demonstrated by Ryan Gordon
Demonstrates how CACAO Security Playbooks can integrate Ansible playbooks or modules to leverage the existing Open Security Community.


