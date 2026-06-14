from kubert import cluster, prereq
from kubert.ui import show_failure, show_info, show_success, show_title


def init_cluster() -> bool:
    show_title("Checking prerequisites")
    tools = prereq.check_all()
    for t in tools:
        if t.installed:
            show_success(f"{t.name} found")
        else:
            show_failure(f"{t.name} missing - install: {t.install_url}")
    if not all(t.installed for t in tools):
        return False
    if cluster.exists():
        show_info(f"Cluster '{cluster.name()}' already exists.")
        return True
    show_title("Creating Kind cluster")
    cluster.create()
    show_success("Cluster ready.")
    return True
