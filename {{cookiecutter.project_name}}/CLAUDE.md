# Claude Code Rules for test-docker-app

## Project Overview

This is a **FastAPI + Tortoise ORM** production application.

**Tech Stack:**
- Python 3.11+
- FastAPI (async web framework)
- Tortoise ORM with asyncpg (NOT SQLAlchemy!)
- Aerich (database migrations)
- Poetry (dependency management)
- Ruff (linting and formatting)
- Pytest (testing framework)

---

## 🚨 NO-TOUCH ZONES

**NEVER modify these files without EXPLICIT user permission:**

### Critical Configuration
- `pyproject.toml` - dependency management, DO NOT auto-update dependencies
- `poetry.lock` - locked dependencies, DO NOT regenerate without permission
- `.env` - environment secrets, NEVER read or modify
- `.env.example` - template file, can read but ask before modifying

### Database & Migrations
- `app/db/migrations/` - NEVER edit migration files manually!
- `app/config/components/db.py` - database config, ask before changes
- `app/db/models/` - existing models can be extended, but ask before breaking changes

### Production & Deployment
- `Dockerfile` - deployment config, ask before modifying
- `docker-compose.yml` - orchestration, ask before modifying

---

## ✅ QUALITY GATES

**Before ANY commit, ALL of these must pass:**

### 1. Code Formatting
```bash
poetry run ruff format .
```
**Must succeed with zero changes needed.**

### 2. Linting
```bash
poetry run ruff check . --fix
```
**Must pass with zero errors.** Auto-fix what you can, manually fix the rest.

### 3. Type Checking (if mypy available)
```bash
poetry run mypy app/ --ignore-missing-imports
```
**Zero errors allowed.** Use `# type: ignore` ONLY with explanation comment.

### 4. Tests
```bash
poetry run pytest tests/ -v
```
**All tests must pass.** NO skipping tests. NO `@pytest.mark.skip` without issue link.

### 5. Test Coverage
```bash
poetry run pytest tests/ --cov=app --cov-report=term-missing
```
**Minimum 80% coverage overall.** New code should have 90%+ coverage.

---

## 🛡️ REGRESSION PREVENTION RULES

### Rule 1: ONE Change at a Time
- **DO:** Focus on one feature/bugfix per conversation
- **DON'T:** "While I'm here, let me also refactor..."
- **Exception:** Only if user explicitly asks for broader changes

### Rule 2: List Affected Files BEFORE Writing Code
Before making any changes, ALWAYS:
1. List ALL files that will be modified
2. Explain WHAT will change in each file
3. Wait for user confirmation if more than 3 files affected

### Rule 3: No "Improvements" to Working Code
- **DO:** Fix requested bugs or add requested features
- **DON'T:** Refactor code that wasn't mentioned
- **DON'T:** "Improve" variable names, add comments, or reorganize unless asked
- **Exception:** Only fix if it directly impacts your current task

### Rule 4: Migrations Must Be Generated
- **DO:** Change model → generate migration with aerich
- **DON'T:** Edit existing migrations
- **Command:** `poetry run aerich migrate --name "descriptive_name"`

### Rule 5: Ask Before Breaking Changes
**Breaking changes require confirmation:**
- Changing function signatures
- Removing fields from models
- Changing API response structure
- Updating dependencies to major versions
- Modifying authentication logic

---

## 📝 CODING STANDARDS

### Type Hints (Mandatory!)
```python
# ❌ Bad - no type hints
def get_user(id):
    return User.get(id)

# ✅ Good - full type hints
async def get_user(user_id: int) -> User | None:
    """Get user by ID."""
    return await User.get_or_none(id=user_id)
```

### Docstrings (Required for Public Functions)
```python
def create_user(username: str, email: str) -> User:
    """Create a new user.
    
    Args:
        username: Unique username (3-50 chars)
        email: Valid email address
        
    Returns:
        Created User instance
        
    Raises:
        IntegrityError: If username/email already exists
        ValueError: If validation fails
    """
    ...
```

### Modern Python (3.11+)
```python
# ✅ Use new syntax
list[str]           # Not List[str]
dict[str, int]      # Not Dict[str, int]
User | None         # Not Optional[User]
str | int           # Not Union[str, int]

# ✅ Use from collections.abc
from collections.abc import Sequence, Mapping
```

### Async/Await Everywhere
```python
# ❌ Bad - synchronous style won't work
user = User.objects.get(id=1)

# ✅ Good - async/await required
user = await User.get(id=1)
users = await User.all()
users = await User.filter(is_active=True)
```

### Pydantic Response Models
```python
# ❌ Bad - returning raw dict
@router.get("/users/{user_id}")
async def get_user(user_id: int):
    user = await User.get(id=user_id)
    return {"id": user.id, "name": user.username}

# ✅ Good - Pydantic model
class UserResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    
    id: int
    username: str
    email: str

@router.get("/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: int) -> UserResponse:
    user = await User.get(id=user_id)
    return UserResponse.model_validate(user)
```

### Error Handling
```python
from fastapi import HTTPException, status

# ✅ Always handle DoesNotExist
from tortoise.exceptions import DoesNotExist

try:
    user = await User.get(id=user_id)
except DoesNotExist:
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"User {user_id} not found",
    )
```

---

## 🔐 SECURITY RULES

### Never Hardcode Secrets
```python
# ❌ NEVER do this
API_KEY = "sk-proj-1234567890"
PASSWORD = "admin123"

# ✅ Always use environment variables in pydantic settings
API_KEY = os.getenv("API_KEY")
PASSWORD = settings.database_password
```

### Validate All Inputs
```python
# ✅ Use Pydantic for validation
class UserCreate(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=8)
```

---

## 🧪 TESTING REQUIREMENTS

### Test File Structure
```
tests/
├── conftest.py          # Fixtures
├── test_api/            # API endpoint tests
│   ├── test_users.py
│   └── test_auth.py
└── test_models/         # Model tests
    └── test_user.py
```

### Async Test Example
```python
import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_get_user(client: AsyncClient, test_user: User) -> None:
    """Test GET /users/{id} endpoint."""
    response = await client.get(f"/api/v1/users/{test_user.id}")
    
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == test_user.username
    assert data["email"] == test_user.email
```

### Test Coverage Requirements
- **Minimum:** 80% overall coverage
- **New code:** 90%+ coverage
- **Critical paths:** 100% coverage (auth, payments, core business logic)

---

## 🚀 WORKFLOW

### Adding a New Feature
1. **Understand requirements** - ask clarifying questions
2. **List affected files** - before writing any code
3. **Write tests first** (TDD approach preferred)
4. **Implement feature** with type hints and docstrings
5. **Run quality gates** - all must pass
6. **Generate migration** if models changed
7. **Update API docs** if new endpoints added
8. **Commit** with descriptive message

### Fixing a Bug
1. **Reproduce bug** with failing test
2. **Identify root cause** - don't guess
3. **Fix the bug** - minimal changes
4. **Verify test passes** - bug no longer reproducible
5. **Run quality gates** - ensure no regressions
6. **Commit** with "fix:" prefix

### Database Changes
```bash
# 1. Modify model in code
# 2. Generate migration
poetry run aerich migrate --name "add_user_status"
# 3. Review generated migration
# 4. Apply migration
poetry run aerich upgrade
# 5. Test migration is reversible
poetry run aerich downgrade
poetry run aerich upgrade
```

---

## 💡 BEST PRACTICES

### Dependency Injection
```python
from typing import Annotated
from fastapi import Depends

# Define type alias
CurrentUser = Annotated[User, Depends(get_current_user)]

@router.get("/profile")
async def get_profile(user: CurrentUser) -> UserResponse:
    """Get current user profile."""
    return UserResponse.model_validate(user)
```

### Database Queries
```python
# ✅ Use select_for_update for atomic operations
async with in_transaction():
    user = await User.get(id=user_id).select_for_update()
    user.balance += amount
    await user.save()

# ✅ Use efficient filtering
users = await User.filter(
    is_active=True,
    created_at__gte=datetime.now() - timedelta(days=30)
).order_by("-created_at").limit(100)
```

### Error Messages
```python
# ❌ Bad - vague error
raise HTTPException(status_code=400, detail="Invalid input")

# ✅ Good - specific error
raise HTTPException(
    status_code=status.HTTP_400_BAD_REQUEST,
    detail="Username must be between 3 and 50 characters",
)
```

---

## 🐛 DEBUGGING

### Enable Debug Logging
```python
import logging

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Use in code
logger.debug(f"User {user_id} request received")
logger.info(f"User {user_id} created successfully")
logger.error(f"Failed to create user: {error}")
```

---

## 📊 PERFORMANCE

### Query Optimization
```python
# ❌ N+1 queries
users = await User.all()
for user in users:
    posts = await user.posts.all()  # Separate query for each user!

# ✅ Prefetch relations
users = await User.all().prefetch_related("posts")
for user in users:
    posts = await user.posts  # No additional query!
```

### Async Operations
```python
import asyncio

# ❌ Sequential (slow)
user1 = await User.get(id=1)
user2 = await User.get(id=2)

# ✅ Concurrent (fast)
user1, user2 = await asyncio.gather(
    User.get(id=1),
    User.get(id=2),
)
```

---

## 🔄 ROLLBACK PROCEDURE

If something breaks:

### 1. Immediate Rollback (Git)
```bash
# Undo last commit
git reset --soft HEAD~1

# Undo all changes
git reset --hard HEAD
```

### 2. Database Rollback
```bash
# Rollback last migration
poetry run aerich downgrade

# Rollback to specific version
poetry run aerich history  # Find version
poetry run aerich downgrade --version 3
```

### 3. Verify
```bash
# Run tests to verify stability
poetry run pytest tests/ -v

# Check application starts
poetry run uvicorn app.main:app --reload
```

---

## 🎯 REMEMBER

1. **Quality gates are not optional** - they must ALL pass
2. **No-touch zones are sacred** - ask before modifying
3. **One change at a time** - no scope creep
4. **Tests are required** - no code without tests
5. **Type hints everywhere** - no exceptions
6. **Async/await required** - this is an async codebase
7. **Never commit secrets** - use environment variables
8. **Migrations never edited** - always generate new ones

---

## 📚 PROJECT-SPECIFIC NOTES

### Poetry Commands
```bash
# Install dependencies
poetry install

# Add dependency
poetry add package-name

# Add dev dependency
poetry add --group dev package-name

# Update dependencies (ASK FIRST!)
poetry update

# Run commands
poetry run python script.py
poetry run pytest tests/
```

### Environment Setup
```bash
# 1. Copy .env.example to .env
cp .env.example .env

# 2. Fill in secrets
vim .env

# 3. Install dependencies
poetry install

# 4. Run migrations
poetry run aerich upgrade

# 5. Start development server
poetry run uvicorn app.main:app --reload
```

---

**This is a production codebase. Treat it with respect.**

✅ Write clean, tested, documented code
✅ Follow all quality gates
✅ Ask when uncertain
✅ Respect no-touch zones

❌ No shortcuts
❌ No "I'll fix it later"
❌ No breaking things without tests