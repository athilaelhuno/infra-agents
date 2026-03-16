import re

def test_tf_plan_parser():
    stdout = """
Terraform used the selected providers to generate the following execution plan.
Resource actions are indicated with the following symbols:
  + create

Terraform will perform the following actions:

  # null_resource.test will be created
  + resource "null_resource" "test" {
      + id = (known after apply)
    }

Plan: 1 to add, 0 to change, 0 to destroy.
"""
    match = re.search(r"Plan: (\d+) to add, (\d+) to change, (\d+) to destroy", stdout)
    assert match is not None
    assert int(match.group(1)) == 1
    assert int(match.group(2)) == 0
    assert int(match.group(3)) == 0

def test_kube_pod_parser():
    stdout = """
pod1  1/1  Running    0  10m
pod2  0/1  Error      0  5m
pod3  1/1  Running    0  1m
"""
    failing = []
    lines = stdout.strip().split("\n")
    for line in lines:
        parts = line.split()
        if len(parts) >= 3:
            name, ready, status = parts[0], parts[1], parts[2]
            if status != "Running" and status != "Completed":
                failing.append({"name": name, "status": status})
    
    assert len(failing) == 1
    assert failing[0]["name"] == "pod2"
