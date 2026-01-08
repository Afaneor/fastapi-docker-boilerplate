---
name: strict-python-mode
description: Enforces type hints, docstrings, and Python best practices. Use when writing or refactoring Python code, creating new functions, or when user mentions "production-ready" or "type-safe" code.
allowed-tools: Edit, Write, Read, Bash(ruff:*, mypy:*)
---

# Strict Python Mode

## Core Principles

When writing Python code in this project, ALWAYS follow these rules:

1. **Type hints are mandatory**
   - Every function parameter must have a type hint
   - Every function must have a return type annotation
   - Use `from collections.abc import` for generic types (list, dict, set)
   - Never use `Any` type - if type is unknown, use `object` or create proper Protocol

2. **Docstrings are required**
   - Every public function/method needs a docstring
   - Use Google-style docstrings format
   - Include Args, Returns, Raises sections

3. **Modern Python syntax (3.12+)**
   - Use `list[str]` instead of `List[str]` from typing
   - Use `dict[str, int]` instead of `Dict[str, int]`
   - Use `X | None` instead of `Optional[X]`
   - Use `X | Y` for Union types

## Code Quality Checks

Before finishing ANY code changes, run these checks:

```bash
# 1. Format with Ruff
poetry run ruff format .

# 2. Lint with Ruff
poetry run ruff check . --fix

# 3. Type check with mypy (if available)
poetry run mypy app/ --ignore-missing-imports
```

## Example: Good vs Bad

### ❌ Bad (will be rejected)
```python
def get_user(id):
    user = db.get(id)
    return user
```

### ✅ Good (approved)
```python
def get_user(user_id: int) -> User | None:
    """Fetch user by ID from database.
    
    Args:
        user_id: The unique identifier of the user
        
    Returns:
        User object if found, None otherwise
        
    Raises:
        DatabaseError: If database connection fails
    """
    user = db.get(user_id)
    return user
```

## FastAPI-Specific Rules

### Endpoint Signatures
```python
# Always use dependency injection
@router.get("/users/{user_id}")
async def get_user(
    user_id: int,
    db: DatabaseSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
) -> UserResponse:
    """Get user by ID."""
    ...
```

### Response Models
```python
# Always define explicit response models
class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True
```

## Validation Rules

Before ANY commit:
1. All new functions have type hints
2. All public functions have docstrings
3. Ruff format passes with no changes needed
4. Ruff check passes with no errors
5. If mypy is available, it passes with no errors

If any check fails, FIX IT before showing me the code.