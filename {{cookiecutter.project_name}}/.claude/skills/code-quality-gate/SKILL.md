---
name: code-quality-gate
description: Automated code quality checks before commits. Use before committing code, when finishing a feature, or when user mentions "ready to commit" or "quality check".
allowed-tools: Bash(poetry:*, ruff:*, pytest:*)
hooks:
  Stop:
    - matcher: ""
      hooks:
        - type: command
          command: "poetry run ruff format . && poetry run ruff check . && poetry run pytest tests/ -v"
---

# Code Quality Gate

## 5-Stage Quality Pipeline

Before ANY commit, code must pass ALL stages. No exceptions.

### Stage 1: Code Formatting (Ruff Format)
```bash
poetry run ruff format .
```
**What it checks:**
- Consistent code style (PEP 8 compliant)
- Line length (88 characters by default)
- Imports formatting
- Trailing whitespace

**Action:** Auto-fixes issues. Re-run if changes were made.

### Stage 2: Linting (Ruff Check)
```bash
poetry run ruff check . --fix
```
**What it checks:**
- Unused imports and variables
- Code smells and anti-patterns
- Security issues (hardcoded secrets, SQL injection)
- Complexity issues
- Missing docstrings

**Action:** Auto-fixes when possible. Manual fixes required for some issues.

### Stage 3: Type Checking (MyPy) - Optional
```bash
poetry run mypy app/ --ignore-missing-imports || true
```
**What it checks:**
- Type hint correctness
- Return type mismatches
- Argument type errors
- None-safety violations

**Action:** Fix type errors. Use `# type: ignore` only as last resort with comment explaining why.

### Stage 4: Tests (Pytest)
```bash
poetry run pytest tests/ -v --maxfail=1
```
**What it checks:**
- All tests pass
- No test failures
- No test errors

**Action:** Fix failing tests. Never skip tests.

### Stage 5: Import Sorting
```bash
poetry run ruff check . --select I --fix
```
**What it checks:**
- Import order (stdlib → third-party → local)
- Import grouping
- Unused imports

**Action:** Auto-fixes import order.

## Full Quality Gate Command

Run all stages in sequence:
```bash
poetry run ruff format . && \
poetry run ruff check . --fix && \
poetry run pytest tests/ -v && \
echo "✅ All quality checks passed!"
```

## When to Run Quality Gates

### 1. Before Every Commit
```bash
# Before git commit
./run_quality_gate.sh
git add .
git commit -m "feat: add user endpoint"
```

### 2. After Major Refactoring
```bash
# After large code changes
poetry run pytest tests/ -v --cov=app --cov-report=html
```

### 3. Before Pull Request
```bash
# Full comprehensive check
poetry run ruff check . --statistics
poetry run pytest tests/ -v --cov=app --cov-report=term-missing
```

## What to Do When Checks Fail

### Ruff Format Failures
If `ruff format` makes changes:
```bash
poetry run ruff format .
git add .  # Stage formatted files
```

### Ruff Check Failures
Read error messages carefully:
```
app/api/users.py:45:5: F401 'User' imported but unused
```

Fix the issue:
```python
# Remove unused import
# from models import User  ← Remove this
```

### Pytest Failures
```
FAILED tests/test_users.py::test_get_user - AssertionError: ...
```

Debug and fix:
```bash
# Run specific test with output
poetry run pytest tests/test_users.py::test_get_user -v -s
```

### Type Check Failures (MyPy)
```
app/api/users.py:45: error: Incompatible return value type
```

Fix type annotations:
```python
# Before (wrong)
def get_user(id) -> User:
    return None  # Error: None is not User!

# After (correct)
def get_user(id: int) -> User | None:
    return None  # OK: None is allowed
```

## Coverage Requirements

Maintain minimum test coverage:
- **Overall coverage:** 80%+
- **New code coverage:** 90%+
- **Critical paths:** 100% (auth, payments, etc.)

Check coverage:
```bash
poetry run pytest tests/ --cov=app --cov-report=term-missing
```

## Emergency Bypass (Use Sparingly!)

In rare cases when quality gate blocks urgent fixes:
```bash
# Skip only specific check
poetry run ruff check . --ignore E501  # Ignore line length

# Or commit with --no-verify (DOCUMENT WHY!)
git commit -m "hotfix: critical bug" --no-verify
```

**Rules for bypass:**
1. Document reason in commit message
2. Create follow-up issue to fix properly
3. Never bypass tests
4. Get team approval for production

## Quality Gate Success Criteria

All of these must be true:
- ✅ `ruff format .` makes zero changes
- ✅ `ruff check .` returns zero errors
- ✅ `mypy app/` returns zero errors (if enabled)
- ✅ `pytest tests/` all tests pass
- ✅ Test coverage ≥ 80%

## Troubleshooting

### "Command not found: ruff"
```bash
poetry install  # Install dependencies first
```

### "No tests collected"
```bash
# Check test file naming
# Must be: test_*.py or *_test.py
ls tests/
```

### "Import errors in tests"
```bash
# Set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
poetry run pytest tests/
```

### Slow tests
```bash
# Run in parallel
poetry run pytest tests/ -n auto

# Run only fast tests
poetry run pytest tests/ -m "not slow"
```

## Pre-commit Hook Setup (Optional)

Create `.git/hooks/pre-commit`:
```bash
#!/bin/bash
echo "Running quality gate..."
poetry run ruff format .
poetry run ruff check . --fix
poetry run pytest tests/ -v --maxfail=1

if [ $? -ne 0 ]; then
    echo "❌ Quality gate failed. Commit blocked."
    exit 1
fi

echo "✅ Quality gate passed!"
```

Make it executable:
```bash
chmod +x .git/hooks/pre-commit
```

## Integration with CI/CD

Quality gate should also run in CI:
```yaml
# .github/workflows/quality.yml
name: Quality Gate
on: [push, pull_request]
jobs:
  quality:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - run: poetry install
      - run: poetry run ruff format . --check
      - run: poetry run ruff check .
      - run: poetry run pytest tests/ --cov=app
```

## Remember

**Quality gate is not optional.** It's the foundation of production-ready code.

No shortcuts. No bypasses. No "I'll fix it later."

✅ Write code → Run quality gate → Fix issues → Commit → Repeat