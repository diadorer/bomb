.PHONY: release
release:
	@bash scripts/release.sh minor


.PHONY: hotrix
hotfix:
	@bash scripts/release.sh patch
