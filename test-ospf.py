from nornir import InitNornir
from nornir_scrapli.tasks import send_command
from nornir_utils.plugins.functions import print_result
import os
import sys


config_file = sys.argv[1]

nr = InitNornir(config_file=config_file)

nr.inventory.defaults.username = os.getenv("USERNAME")
nr.inventory.defaults.password = os.getenv("PASSWORD")

def pull_info (task):
    response = task.run(task=send_command, command= "show ip ospf neighbor")
    task.host['facts'] = response.scrapli_response.genie_parse_output()
    interfaces = task.host['facts']['interfaces']
    for int in interfaces:
        neighbors = interfaces[int]['neighbors']
        for neighbor in neighbors:
            state = neighbors[neighbor]['state']
            return state



result = nr.run(task=pull_info)

for host in nr.inventory.hosts.values():
    state = result[f"{host}"][0].result
    assert "FULL" in state, "FAILED"
print("PASSED")



