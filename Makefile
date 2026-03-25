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
	@echo ""

install:
	@echo "Installing dependencies..."
	pnpm install

run: install
	pnpm run docs:dev

build: install clean aggregate
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
	@# Clean aggregated (untracked) content from section directories, preserving git-tracked files
	@if [ -d .git ]; then \
		git clean -fd docs/contributing/ docs/explanation/ docs/how-to/ docs/reference/ docs/tutorials/ 2>/dev/null || true; \
	else \
		rm -rf docs/contributing docs/explanation docs/how-to docs/reference docs/tutorials; \
	fi
	@echo "Clean complete!"
