GO ?= go
PACKAGE ?= ./...

.PHONY: fmt-check unit unit-package vet build check

fmt-check:
	@files="$$(find . -name '*.go' -type f -not -path './vendor/*')"; \
	if [ -z "$$files" ]; then echo "no Go files; skip fmt-check"; \
	else test -z "$$(gofmt -l $$files)"; fi

unit:
	@pkgs="$$($(GO) list ./... 2>/dev/null || true)"; \
	if [ -z "$$pkgs" ]; then echo "no Go packages; skip unit"; \
	else $(GO) test ./...; fi

unit-package:
	@test "$(PACKAGE)" != "./..." || (echo "set PACKAGE, e.g. make unit-package PACKAGE=./internal/foo"; exit 2)
	$(GO) test $(PACKAGE)

vet:
	@pkgs="$$($(GO) list ./... 2>/dev/null || true)"; \
	if [ -z "$$pkgs" ]; then echo "no Go packages; skip vet"; \
	else $(GO) vet ./...; fi

build:
	@pkgs="$$($(GO) list ./... 2>/dev/null || true)"; \
	if [ -z "$$pkgs" ]; then echo "no Go packages; skip build"; \
	else $(GO) build ./...; fi

check: fmt-check unit vet build
