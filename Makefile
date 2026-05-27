.PHONY: smoke public-check

smoke:
	bash scripts/run_smoke_test.sh

public-check: smoke
	python -m compileall -q scripts
	@if grep -RIn --exclude-dir=.git --exclude='*.pdf' --exclude='*.zip' --exclude='Makefile' '/Users/fu\|/private/var/folders\|OPENAI_API_KEY\|ANTHROPIC_API_KEY' .; then \
		echo "Found private path or secret-like string." >&2; exit 1; \
	fi
