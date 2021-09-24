.PHONY: prerelease
prerelease:
	@poetry run python scripts/release.py prerelease


.PHONY: release/preminor
release/preminor:
	@poetry run python scripts/release.py preminor


.PHONY: prepatch-release
prepatch-release:
	@poetry run python scripts/release.py prepatch


.PHONY: minor-release
minor-release:
	@poetry run python scripts/release.py minor


.PHONY: patch-release
patch-release:
	@poetry run python scripts/release.py patch

