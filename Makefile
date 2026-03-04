.PHONY: run help

help:
	@echo "Available targets:"
	@echo "		run - Run docs locally"

run:
	pnpm run docs:dev