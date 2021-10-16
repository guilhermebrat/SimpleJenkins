from nornir import InitNornir
from nornir_scrapli.tasks import send_configs
from nornir_utils.plugins.functions import print_result
from nornir.core.exceptions import NornirExecutionError
from nornir_jinja2.plugins.tasks import template_file
from nornir_utils.plugins.tasks.data import load_yaml


nr = InitNornir(config_file="config.yaml")

def pull_vars(task):
    results = task.run(task=load_yaml, file="group_vars/all.yaml")
    task.host['facts'] = results.result
    push_config(task)

def push_config(task):
    ospf_config = task.run (task=template_file, template="ospf.j2", path="templates")
    configurations = ospf_config.result.splitlines()
    task.run(task=send_configs, configs=configurations)


response = nr.run(task=pull_vars)
print_result(response)
failures = nr.data.failed_hosts
if failures:
    raise NornirExecutionError("Nornir Failure Detected")