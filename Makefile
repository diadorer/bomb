.PHONY: prerelease
prerelease:
	@poetry run python scripts/release.py prerelease

.PHONY: preminor
preminor:
	@poetry run python scripts/release.py preminor


.PHONY: prepatch
prepatch:
	@poetry run python scripts/release.py prepatch


.PHONY: minor
minor:
	@poetry run python scripts/release.py minor


.PHONY: patch
patch:
	@poetry run python scripts/release.py patch
