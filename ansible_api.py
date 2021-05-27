# -*- coding: utf-8 -*-
# pragma pylint: disable=unused-argument, no-self-use
# Adapted from https://github.com/ibmResilient/resilient-community-apps/blob/master/fn_ansible/fn_ansible/lib/ansible_api.py
# permitted by the MIT license, copy of such here amended with additional author info
# Copyright © IBM Corporation 2010, 2021
# Copyright © Ryan Gordon 2021
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to
# deal in the Software without restriction, including without limitation the
# rights to use, copy, modify, merge, publish, distribute, sublicense, and/or
# sell copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS
# IN THE SOFTWARE.

"""
This module intends to provide a high level API
for Ansible's core level modules and their functionalities.
"""

import ansible_runner
import functools
import logging
import os
import shutil
import sys
import tempfile

if sys.version_info[0] >= 3:
    import html as HTMLParser
    h = HTMLParser
else:
    from HTMLParser import HTMLParser
    h = HTMLParser()

log = logging.getLogger(__name__)

def private_dir(func):
    """
    Make a private, writable copy of the ansible directory of hosts, secrets, yml playbooks per each invocation
    :return: temporary directory used
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        with tempfile.TemporaryDirectory() as fp:
            new_dir = os.path.join(fp, "private")
            shutil.copytree(kwargs['private_data_dir'], new_dir)
            kwargs['private_data_dir'] = new_dir
            return func(*args, **kwargs)

    return wrapper

@private_dir
def run_playbook(
        id=None,
        private_data_dir=None,
        artifact_dir=None,
        playbook_name=None,
        playbook_args=None,
        module_name=None,
        module_args=None,
        module_hosts=None,
        **kwargs
    ):
    """This function is responsible for running a playbook
    and returns the results of the queries that the playbook
    contains.
    """

    result = {}
    try:
        if playbook_name:
            log.info(u"Running playbook '%s' with ID %s", playbook_name, id)
            r = ansible_runner.run(ident=id,
                                   private_data_dir=private_data_dir,
                                   artifact_dir=artifact_dir,
                                   playbook=playbook_name,
                                   extravars=playbook_args,
                                   **kwargs
                                   )
        elif module_name:
            log.info(u"Running module '%s' with ID %s", module_name, id)
            r = ansible_runner.run(ident=id,
                                   private_data_dir=private_data_dir,
                                   artifact_dir=artifact_dir,
                                   module=module_name,
                                   module_args=module_args,
                                   host_pattern=module_hosts,
                                   **kwargs
                                   )

        for host in r.events:
            log.debug(host)
            if sys.version_info[0] >= 3:
                detail = bytes(host.get('stdout', ''), 'utf-8').decode('unicode_escape')
            else:
                detail = host.get('stdout', '').decode('string_escape')

            if host.get('event', '').startswith('runner_on'):
                # look for json results
                if host['event_data'].get("res"):
                    detail = host['event_data'].get("res")

                result[host['event_data']['host']] = {
                    'summary': r.status,
                    'detail': detail
                }
            elif host.get('event', '') in ('verbose', 'error'):
                result[host['runner_ident']] = {
                    'summary': r.status,
                    'detail': detail
                }

        return result

    except Exception as original_exception:
        raise ValueError(original_exception)


def cleanup_artifact_dir(path, num):
    # navigate to directory for artifacts
    artifacts_path = os.path.join(path, 'artifacts')
    ansible_runner.utils.cleanup_artifact_dir(artifacts_path, num_keep=num)
