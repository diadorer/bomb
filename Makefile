.PHONY: prerelease
prerelease:
	@poetry run python scripts/release.py prerelease


.PHONY: release/preminor
release/preminor:
	@poetry run python scripts/release.py preminor


.PHONY: release/prepatch
release/prepatch:
	@poetry run python scripts/release.py prepatch


.PHONY: release/minor
release/minor:
	@poetry run python scripts/release.py minor


.PHONY: release/patch
release/patch:
	@poetry run python scripts/release.py patch

