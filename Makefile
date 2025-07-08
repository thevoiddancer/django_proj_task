lint:
	@clear
	@echo "Running ruff on budget_app"
	@ruff check --fix budget_app/ || true
	@echo "Running ruff on home_budget"
	@ruff check --fix home_budget/ || true
	@echo "Running ruff on tests"
	@ruff check --fix tests/ || true
	@echo "Running mypy on budget_app"
	@poetry run mypy budget_app/ || true
	@echo "Running mypy on home_budget"
	@poetry run mypy home_budget/ || true
	@echo "Running mypy on tests"
	@poetry run mypy tests/ || true

format:
	@clear
	@echo "Running ruff format on budget_app"
	@ruff format budget_app/ || true
	@echo "Running ruff format on home_budget"
	@ruff format home_budget/ || true
	@echo "Running ruff format on tests"
	@ruff format tests/ || true

format-diff:
	@clear
	@echo "Running ruff format on budget_app"
	@ruff format -diff budget_app/ || true
	@echo "Running ruff format on home_budget"
	@ruff format -diff home_budget/ || true
	@echo "Running ruff format on tests"
	@ruff format -diff tests/ || true
