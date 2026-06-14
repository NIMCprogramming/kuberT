import shutil
from dataclasses import dataclass


@dataclass
class Tool:
    name: str
    install_url: str
    installed: bool = False


_TOOLS = [
    ("docker", "https://docs.docker.com/engine/install/ubuntu/"),
    ("kind", "https://kind.sigs.k8s.io/docs/user/quick-start/#installation"),
    ("kubectl", "https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/"),
]


def check_all() -> list[Tool]:
    return [Tool(n, u, shutil.which(n) is not None) for n, u in _TOOLS]
