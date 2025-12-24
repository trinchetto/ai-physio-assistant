# Task Completion Checklist

## Before Committing Code
1. Run all tests: `poetry run pytest`
2. Check linting: `poetry run ruff check src/`
3. Format code: `poetry run ruff format src/`
4. Type check: `poetry run mypy src/`
5. Or run all at once: `poetry run pre-commit run --all-files`

## Code Quality Requirements
- All type hints must be complete
- No lines longer than 100 characters
- All tests must pass
- No linting errors
- No type checking errors

## Testing Requirements
- New features must include tests
- Aim for meaningful test coverage
- Test validation errors appropriately
