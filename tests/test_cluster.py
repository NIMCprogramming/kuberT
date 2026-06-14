import subprocess
from unittest.mock import patch

from kubert import cluster


def test_name_default(monkeypatch) -> None:
    monkeypatch.delenv("KUBERT_CLUSTER_NAME", raising=False)
    assert cluster.name() == "kubert"


def test_name_from_env(monkeypatch) -> None:
    monkeypatch.setenv("KUBERT_CLUSTER_NAME", "custom")
    assert cluster.name() == "custom"


def test_node_image_default(monkeypatch) -> None:
    monkeypatch.delenv("KUBERT_NODE_IMAGE", raising=False)
    assert cluster.node_image() == "kindest/node:v1.32.2"


def test_node_image_from_env(monkeypatch) -> None:
    monkeypatch.setenv("KUBERT_NODE_IMAGE", "kindest/node:v1.30.0")
    assert cluster.node_image() == "kindest/node:v1.30.0"


@patch("kubert.cluster.subprocess.run")
def test_list_clusters_empty(mock_run) -> None:
    mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="", stderr="")
    assert cluster.list_clusters() == []


@patch("kubert.cluster.subprocess.run")
def test_list_clusters_parsed(mock_run) -> None:
    mock_run.return_value = subprocess.CompletedProcess(
        args=[], returncode=0, stdout="kubert\nother\n", stderr=""
    )
    assert cluster.list_clusters() == ["kubert", "other"]


@patch("kubert.cluster.subprocess.run")
def test_list_clusters_handles_kind_failure(mock_run) -> None:
    mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=1, stdout="", stderr="")
    assert cluster.list_clusters() == []


@patch("kubert.cluster.list_clusters", return_value=["kubert"])
def test_exists_true(_mock_list) -> None:
    assert cluster.exists() is True


@patch("kubert.cluster.list_clusters", return_value=["other"])
def test_exists_false(_mock_list) -> None:
    assert cluster.exists() is False


@patch("kubert.cluster.subprocess.run")
def test_is_reachable_true(mock_run) -> None:
    mock_run.return_value = subprocess.CompletedProcess(args=[], returncode=0, stdout="ok", stderr="")
    assert cluster.is_reachable() is True


@patch("kubert.cluster.subprocess.run")
def test_is_reachable_false_on_nonzero_exit(mock_run) -> None:
    mock_run.return_value = subprocess.CompletedProcess(
        args=[], returncode=1, stdout="", stderr="refused"
    )
    assert cluster.is_reachable() is False
