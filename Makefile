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

.PHONY:
prep prepare:
	git diff --exit-code
	git pull
	poetry version patch	# Bump minor version (assuming release within the same month)
	./tools/update_changelog.py
	git commit -a -m "Release $$(poetry version)"
	git tag "v$$(poetry version --short)"
	git diff origin HEAD
	git tag --points-at HEAD
	@echo "\033[0;33mPlease,verify changes and if everything is OK, execute\033[0m"
	@echo "\033[0;31mgit push && git push --tags \033[0m"
