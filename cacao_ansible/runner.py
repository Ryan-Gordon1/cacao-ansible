from ansible_api import run_playbook, cleanup_artifact_dir
from uuid import uuid4

IS_MODULE = False
DEFAULT_PLAYBOOK_NAME = "search_system_for_file.yml"
DEFAULT_ARTIFACT_DIR = "/tmp"
DEFAULT_RUNNER_DIR = ""
DEFAULT_PLAYBOOK_JSON = {
    "host_names": "all",
    "artifact_value": "cacao-playbook.jinja2"
}
# Playbooks generally define hosts whereas modules need them on each invocation
DEFAULT_MODULE_HOSTS = ""

def convert_parameters(ansible_parameters):
    """
    convert name=value;name=value syntax to a dictionary
    :param ansible_parameters:
    :return: dictionary
    """
    params_dict = {}

    if ansible_parameters:
        for item in ansible_parameters.split(u";"):
            if len(item.strip(u' ')) > 0:
                k, v = item.split(u"=")
                params_dict[k.strip(u' ')] = v.strip(u' ')

    return params_dict


def convert_ansible_json_to_module(ansible_json):
    """convert_ansible_json_to_module
    helper method to convert a json obj
    into the format modules expect.
    """
    return ' '.join("{!s}={!s}".format(key, val) for (key, val) in ansible_json.items())


def main():
    """main Run the main loop to run a playbook or module
    with information defined in a provided CACAO Playbook.
    This functionality adds a new command type to CACAO
    an ever evolving standard.

    The hope is with this project we can make
    'ansible-json' a part of the spec
    for commands others can benefit from.

    These are the steps we perform :

    To run a playbook we define a number of parameters
    These Params allow you to define a location where your
    remediation playbooks are stored

    Modules have a couple of differences to playbooks
    In order to support both with CACAO we need to
    do some special handling via different kwargs
    """

    # Define the initial common playbook_kwargs
    playbook_kwargs = {
        "id": uuid4(),
        "private_data_dir": DEFAULT_RUNNER_DIR,
        "artifact_dir": DEFAULT_ARTIFACT_DIR
    }
    # If we are dealing with a module, pass in module_args
    if IS_MODULE:
        playbook_kwargs['module_name'] = DEFAULT_PLAYBOOK_NAME
        playbook_kwargs['module_args'] = convert_ansible_json_to_module(
            DEFAULT_PLAYBOOK_JSON)
        playbook_kwargs['module_hosts'] = DEFAULT_MODULE_HOSTS

    else:
        playbook_kwargs['playbook_name'] = DEFAULT_PLAYBOOK_NAME
        playbook_kwargs['playbook_args'] = DEFAULT_PLAYBOOK_JSON

    from models.cacao_ansible_cmd import AnsibleCmdSpec
    from pydantic import ValidationError
    try:
        AnsibleCmdSpec(
            **playbook_kwargs
        )
    except ValidationError as e:
        print(e)
    # Run the playbook with the previously defined args
    playbook_results = run_playbook(**playbook_kwargs)
    print(playbook_results)


if __name__ == "__main__":
    main()
