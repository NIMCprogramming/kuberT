.PHONY: help deps install test lint type init list next reset clean

KIND_VERSION    ?= v0.27.0
KUBECTL_VERSION ?= v1.31.0
ARCH            := $(shell uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
LOCAL_BIN       := $(HOME)/.local/bin

help:
	@echo "make deps      install system deps (kind, kubectl); check docker"
	@echo "make install   install python deps with uv"
	@echo "make test      run pytest"
	@echo "make lint      run ruff check"
	@echo "make type      run mypy"
	@echo "make init      kubert init  (check tools + create cluster)"
	@echo "make next      kubert next  (run next lesson)"
	@echo "make list      kubert list  (list lessons)"
	@echo "make reset     kubert reset (delete cluster)"
	@echo "make clean     delete .venv and caches"

deps:
	@mkdir -p $(LOCAL_BIN)
	@command -v docker >/dev/null || (echo "Install docker: https://docs.docker.com/engine/install/ubuntu/" && exit 1)
	@command -v kind >/dev/null || ( \
		curl -sSLo $(LOCAL_BIN)/kind https://kind.sigs.k8s.io/dl/$(KIND_VERSION)/kind-linux-$(ARCH) && \
		chmod +x $(LOCAL_BIN)/kind && \
		echo "kind -> $(LOCAL_BIN)/kind (add $(LOCAL_BIN) to PATH if needed)" \
	)
	@command -v kubectl >/dev/null || ( \
		curl -sSLo $(LOCAL_BIN)/kubectl https://dl.k8s.io/release/$(KUBECTL_VERSION)/bin/linux/$(ARCH)/kubectl && \
		chmod +x $(LOCAL_BIN)/kubectl && \
		echo "kubectl -> $(LOCAL_BIN)/kubectl (add $(LOCAL_BIN) to PATH if needed)" \
	)
	@echo "System deps ready."

install:
	uv sync --extra dev

test:
	uv run pytest

lint:
	uv run ruff check .

type:
	uv run mypy

init:
	uv run kubert init

next:
	uv run kubert next

list:
	uv run kubert list

reset:
	uv run kubert reset

clean:
	rm -rf .venv .pytest_cache .mypy_cache .ruff_cache
	find . -type d -name __pycache__ -exec rm -rf {} +
