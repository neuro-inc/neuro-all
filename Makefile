.PHONY: setup init
setup init:
	poetry install
	pre-commit install

.PHONY: fmt format
fmt format:
ifdef CI_LINT_RUN
	pre-commit run --all-files --show-diff-on-failure
else
	pre-commit run --all-files
endif


.PHONY: lint
lint: fmt
