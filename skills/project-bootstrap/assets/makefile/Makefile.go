GO ?= go
PACKAGE ?= ./...

.PHONY: fmt-check unit unit-package vet build check

fmt-check:
	@test -z "$$(gofmt -l $$(find . -name '*.go' -type f -not -path './vendor/*'))"

unit:
	$(GO) test ./...

unit-package:
	@test "$(PACKAGE)" != "./..." || (echo "set PACKAGE, e.g. make unit-package PACKAGE=./internal/foo"; exit 2)
	$(GO) test $(PACKAGE)

vet:
	$(GO) vet ./...

build:
	$(GO) build ./...

check: fmt-check unit vet build
