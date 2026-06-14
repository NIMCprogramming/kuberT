import os
import subprocess


def name() -> str:
    return os.getenv("KUBERT_CLUSTER_NAME", "kubert")


def list_clusters() -> list[str]:
    p = subprocess.run(["kind", "get", "clusters"], capture_output=True, text=True, check=False)
    return [c.strip() for c in p.stdout.splitlines() if c.strip()] if p.returncode == 0 else []


def exists() -> bool:
    return name() in list_clusters()


def create() -> None:
    subprocess.run(["kind", "create", "cluster", "--name", name()], check=True)


def delete() -> None:
    subprocess.run(["kind", "delete", "cluster", "--name", name()], check=True)
