.PHONY: help run dev build preview aggregate aggregate-dry aggregate-repo test-aggregate-local clean clean-projects clean-aggregated-git test test-unit test-integration

help:
	@echo "Garden Linux Documentation Hub - Available targets:"
	@echo ""
	@echo "  Development:"
	@echo "    run                    - Run docs development server"
	@echo "    build                  - Build documentation for production"
	@echo "    preview                - Preview production build locally"
	@echo ""
	@echo "  Testing:"
	@echo "    test                   - Run full test suite"
	@echo "    test-unit              - Run unit tests only"
	@echo ""
	@echo "  Documentation Aggregation:"
	@echo "    test-aggregate-local   - Test aggregation with local repos (recommended first)"
	@echo "    aggregate              - Fetch and aggregate docs from all source repos"
	@echo "    aggregate-dry          - Test aggregation without modifying docs/"
	@echo "    aggregate-repo         - Aggregate specific repo (usage: make aggregate-repo REPO=gardenlinux)"
	@echo ""
	@echo "  Utilities:"
	@echo "    clean                  - Clean aggregated docs and build artifacts"
	@echo "    clean-projects         - Remove only aggregated project docs"
	@echo "    clean-aggregated-git   - Remove uncommitted aggregated docs"
	@echo ""

install:
	@echo "Installing dependencies..."
	pnpm install

run: install
	pnpm run docs:dev

build: install
	pnpm run docs:build

preview: install
	pnpm run docs:preview

# Testing
test: install
	@echo "Running full test suite..."
	@cd scripts/tests && ./run_all.sh

test-unit: install
	@echo "Running unit tests..."
	@cd scripts/tests && python3 run_tests.py

# Documentation Aggregation
test-aggregate-local: install
	@echo "Testing aggregation with local repositories..."
	./scripts/test-local.sh --dry-run

aggregate: install
	@echo "Aggregating documentation from source repositories..."
	./scripts/aggregate-docs.sh

aggregate-dry: install
	@echo "Dry run: Testing aggregation without modifying docs directory..."
	./scripts/aggregate-docs.sh --dry-run

aggregate-repo: install
	@if [ -z "$(REPO)" ]; then \
		echo "Error: REPO variable not set"; \
		echo "Usage: make aggregate-repo REPO=gardenlinux"; \
		exit 1; \
	fi
	@echo "Aggregating documentation for repository: $(REPO)"
	./scripts/aggregate-docs.sh --repo $(REPO)

# Utilities
clean:
	@echo "Cleaning build artifacts and aggregated docs..."
	rm -rf docs/.vitepress/dist
	rm -rf docs/.vitepress/cache
	rm -rf docs/projects
	rm -f docs/.vitepress/config.generated.json
	@echo "Clean complete!"
	@echo "Note: VitePress config.mts sidebar entries are not automatically removed."

clean-projects:
	@echo "Removing aggregated project documentation..."
	rm -rf docs/projects
	rm -f docs/.vitepress/config.generated.json
	@echo "Project docs cleaned!"

clean-aggregated-git:
	@echo "Removing uncommitted aggregated documentation..."
	@if [ -d .git ]; then \
		echo "Using git clean to remove untracked files in docs/projects/"; \
		git clean -fd docs/projects/ 2>/dev/null || true; \
		if [ -f docs/.vitepress/config.generated.json ]; then \
			if ! git ls-files --error-unmatch docs/.vitepress/config.generated.json >/dev/null 2>&1; then \
				rm -f docs/.vitepress/config.generated.json; \
				echo "Removed untracked config.generated.json"; \
			fi; \
		fi; \
	else \
		echo "Not a git repository, using regular clean..."; \
		rm -rf docs/projects; \
		rm -f docs/.vitepress/config.generated.json; \
	fi
	@echo "Uncommitted aggregated docs cleaned!"
