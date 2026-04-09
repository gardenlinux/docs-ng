.PHONY: help run dev build preview aggregate aggregate-repo test-aggregate-local clean clean-projects clean-aggregated-git test test-unit test-integration check spelling linkcheck woke

help:
	@echo "Garden Linux Documentation Hub - Available targets:"
	@echo ""
	@echo "  Development:"
	@echo "    run                    - Run docs development server"
	@echo "    build                  - Build documentation for production"
	@echo "    preview                - Preview production build locally"
	@echo ""
	@echo "  Testing:"
	@echo "    test                   - Run full test suite (38 tests: unit + integration)"
	@echo "    test-unit              - Run unit tests only (35 tests)"
	@echo "    test-integration       - Run integration tests only (3 tests)"
	@echo ""
	@echo "  Quality Checks:"
	@echo "    check                  - Run all quality checks (spelling, links, inclusive language)"
	@echo "    spelling               - Check spelling with codespell"
	@echo "    linkcheck              - Check links with lychee"
	@echo "    woke                   - Check inclusive language with woke"
	@echo ""
	@echo "  Documentation Aggregation:"
	@echo "    aggregate-local        - Aggregate from local repos (file:// URLs in repos-config.local.json)"
	@echo "    aggregate              - Aggregate from locked commits (repos-config.json)"
	@echo "    aggregate-update       - Fetch latest from remotes and update commit locks"
	@echo "    aggregate-repo         - Aggregate single repo (usage: make aggregate-repo REPO=gardenlinux)"
	@echo "    aggregate-update-repo  - Update single repo to latest (usage: make aggregate-update-repo REPO=gardenlinux)"
	@echo ""
	@echo "  Utilities:"
	@echo "    clean                  - Clean aggregated docs and build artifacts"
	@echo ""

install:
	@echo "Installing dependencies..."
	pnpm install
	pip install git+https://github.com/gardenlinux/glrd.git@v4.1.0
	pip install git+https://github.com/gardenlinux/python-gardenlinux-lib.git@0.10.20
	pip install -r requirements.txt	

dev: install
	pnpm run docs:dev

build: install clean aggregate
	pnpm run docs:build

preview: install
	pnpm run docs:preview

# Testing
test: test-unit test-integration
	@echo "All tests passed!"

test-unit:
	@echo "Running unit tests..."
	python3 -m pytest tests/unit/ -v

test-integration:
	@echo "Running integration tests..."
	python3 -m pytest tests/integration/ -v

# Quality Checks
check: spelling linkcheck woke
	@echo "All quality checks passed!"

spelling:
	@echo "Running spelling checks..."
	@pnpm run docs:spelling

linkcheck: install
	@echo "Running link checks..."
	@pnpm run docs:linkcheck

woke: install
	@echo "Running inclusive language checks..."
	@pnpm run docs:woke

# Documentation Aggregation
aggregate-local: install
	@echo "Aggregating from local repositories (relative paths)..."
	python3 src/aggregate.py --config repos-config.local.json

aggregate: install
	@echo "Aggregating documentation from locked source repositories..."
	python3 src/aggregate.py

aggregate-update: install
	@echo "Aggregating documentation from latest source repositories..."
	python3 src/aggregate.py --update-locks

aggregate-repo: install
	@if [ -z "$(REPO)" ]; then \
		echo "Error: REPO variable not set"; \
		echo "Usage: make aggregate-repo REPO=gardenlinux"; \
		exit 1; \
	fi
	@echo "Aggregating documentation for locked repository: $(REPO)"
	python3 src/aggregate.py --repo $(REPO)

aggregate-update-repo: install
	@if [ -z "$(REPO)" ]; then \
		echo "Error: REPO variable not set"; \
		echo "Usage: make aggregate-update-repo REPO=gardenlinux"; \
		exit 1; \
	fi
	@echo "Aggregating documentation for locked repository: $(REPO)"
	python3 src/aggregate.py --update-locks --repo $(REPO)

# Utilities
clean:
	@echo "Cleaning build artifacts and aggregated docs..."
	rm -rf docs/.vitepress/dist
	rm -rf docs/.vitepress/cache
	rm -rf docs/projects
	@# Clean aggregated (untracked) content from section directories, preserving git-tracked files
	@if [ -d .git ]; then \
		git clean -fdX docs/contributing/ docs/explanation/ docs/how-to/ docs/reference/ docs/tutorials/ 2>/dev/null || true; \
	else \
		rm -rf docs/contributing docs/explanation docs/how-to docs/reference docs/tutorials; \
	fi
	@echo "Clean complete!"
