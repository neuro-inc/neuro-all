.PHONY: setup init
setup init:
	poetry install
	poetry run pre-commit install

.PHONY: fmt format
fmt format:
ifdef CI_LINT_RUN
	poetry run pre-commit run --all-files --show-diff-on-failure
else
	poetry run pre-commit run --all-files
endif


.PHONY: lint
lint: fmt
