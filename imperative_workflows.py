from typing import List

from flytekit import Workflow, task
from flytekit.remote.remote import FlyteRemote


@task
def t1(a: str) -> str:
    return a + " world"


@task
def t2():
    print("side effect")


@task
def t3(a: List[str]) -> str:
    return ",".join(a)


def new_workflow() -> Workflow:
    wb = Workflow(name="my.imperative.workflow.example")
    wb.add_workflow_input("in1", str)
    node_t1 = wb.add_entity(t1, a=wb.inputs["in1"])
    wb.add_workflow_output("output_from_t1", node_t1.outputs["o0"])
    wb.add_entity(t2)
    wf_in2 = wb.add_workflow_input("in2", str)
    node_t3 = wb.add_entity(t3, a=[wb.inputs["in1"], wf_in2])
    wb.add_workflow_output(
        "output_list",
        [node_t1.outputs["o0"], node_t3.outputs["o0"]],
        python_type=List[str],
    )

    return wb


WORKFLOW: Workflow = new_workflow()
PROJECT_NAME: str = "flytesnacks"
REMOTE_CLUSTER = FlyteRemote(
    "localhost:30081",
    insecure=True,
    default_project=PROJECT_NAME,
    default_domain="staging",
    # image_config=get_image_config(img_name="myapp:v1"),
    # image_config=get_image_config(img_name="mfext:v1"),
)


if __name__ == "__main__":
    print(WORKFLOW)
    print(WORKFLOW(in1="hello", in2="foo"))
