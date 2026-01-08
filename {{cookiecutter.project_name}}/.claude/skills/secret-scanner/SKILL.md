---
name: secret-scanner
description: Detects API keys, passwords, and secrets in code before they reach git. Use before commits, when working with credentials, or when user mentions "security check" or "secrets".
allowed-tools: Bash(git:*, grep:*)
hooks:
  PreToolUse:
    - matcher: "Bash(git commit*)"
      hooks:
        - type: command
          command: |
            git diff --cached --name-only | xargs grep -nHE '(API_KEY|SECRET|PASSWORD|TOKEN|PRIVATE_KEY)\s*=\s*["\047][^"\047]{8,}' && echo "⚠️  Potential secrets detected!" && exit 2 || exit 0
---

# Secret Scanner

## What This Skill Does

Automatically scans code for hardcoded secrets BEFORE they reach git:
- API keys
- Passwords
- Access tokens
- Private keys
- Database credentials
- Any sensitive data

## Detection Patterns

### High-Risk Patterns (Always Block)
```python
# ❌ Will be blocked
API_KEY = "sk_live_1234567890abcdef"
SECRET_KEY = "supersecretpassword123"
PASSWORD = "admin123"
AWS_SECRET = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
PRIVATE_KEY = "-----BEGIN RSA PRIVATE KEY-----"
DATABASE_URL = "postgresql://user:pass@localhost/db"
```

### Safe Patterns (Will Pass)
```python
# ✅ Safe - environment variables
API_KEY = os.getenv("API_KEY")
SECRET_KEY = settings.secret_key
PASSWORD = env.str("DATABASE_PASSWORD")

# ✅ Safe - configuration references
api_key: str = Field(..., env="API_KEY")
```

## Regex Patterns Used

The scanner looks for:
```regex
# API keys and secrets
(API_KEY|SECRET|PASSWORD|TOKEN|PRIVATE_KEY)\s*=\s*["'][^"']{8,}["']

# JWT tokens
eyJ[A-Za-z0-9-_=]+\.eyJ[A-Za-z0-9-_=]+\.[A-Za-z0-9-_.+/=]*

# AWS keys
AKIA[0-9A-Z]{16}

# Database URLs with credentials
(postgres|mysql|mongodb):\/\/[^:]+:[^@]+@

# Private keys
-----BEGIN (RSA|DSA|EC) PRIVATE KEY-----
```

## How to Handle Detected Secrets

### Step 1: Remove from code
```python
# Before (❌ blocked)
OPENAI_KEY = "sk-proj-1234567890abcdef"

# After (✅ passes)
OPENAI_KEY = os.getenv("OPENAI_KEY")
```

### Step 2: Add to .env file
```bash
# .env (never committed!)
OPENAI_KEY=sk-proj-1234567890abcdef
DATABASE_URL=postgresql://user:pass@localhost/db
SECRET_KEY=your-secret-key-here
```

### Step 3: Add to .env.example
```bash
# .env.example (can be committed)
OPENAI_KEY=sk-proj-xxx
DATABASE_URL=postgresql://user:pass@localhost/dbname
SECRET_KEY=generate-with-openssl-rand-hex-32
```

### Step 4: Update .gitignore
```gitignore
# Environment variables
.env
.env.local
.env.production

# Secrets
secrets/
*.key
*.pem
*.cert
```

## Pydantic Settings Integration

Use pydantic-settings for type-safe config:
```python
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """Application settings loaded from environment."""
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
    )
    
    # Database
    database_url: str
    
    # API Keys
    openai_api_key: str
    sentry_dsn: str | None = None
    
    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

# Usage
settings = Settings()
# Now use settings.database_url instead of os.getenv()
```

## Manual Scan Command

Run scanner manually:
```bash
# Scan all Python files
grep -rnE '(API_KEY|SECRET|PASSWORD|TOKEN)\s*=\s*["'\''][^"'\'']{8,}' app/

# Scan staged files only
git diff --cached --name-only | xargs grep -nHE 'API_KEY.*=.*["\047]'

# Check for common patterns
rg 'sk-[a-zA-Z0-9]{20,}' app/  # OpenAI keys
rg 'AKIA[0-9A-Z]{16}' app/     # AWS keys
rg 'ghp_[a-zA-Z0-9]{36}' app/  # GitHub tokens
```

## Common Secret Types

### OpenAI API Keys
```python
# ❌ Bad
OPENAI_KEY = "sk-proj-1234567890"

# ✅ Good
OPENAI_KEY = os.getenv("OPENAI_KEY")
```

### Database Credentials
```python
# ❌ Bad
DATABASE_URL = "postgresql://admin:secretpass@localhost/mydb"

# ✅ Good
DATABASE_URL = settings.database_url
```

### JWT Secrets
```python
# ❌ Bad
SECRET_KEY = "my-super-secret-key-12345"

# ✅ Good
SECRET_KEY = os.getenv("SECRET_KEY")
# Generate with: openssl rand -hex 32
```

### AWS Credentials
```python
# ❌ Bad
AWS_ACCESS_KEY_ID = "AKIAIOSFODNN7EXAMPLE"
AWS_SECRET_ACCESS_KEY = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"

# ✅ Good
# Use AWS CLI credentials or instance roles
import boto3
s3 = boto3.client('s3')  # Uses ~/.aws/credentials
```

## Secrets Already Committed?

If you accidentally committed secrets:

### Step 1: Rotate the secret
```bash
# Generate new API key immediately!
# Old key is now compromised and must be revoked
```

### Step 2: Remove from git history
```bash
# Remove file from all commits
git filter-branch --force --index-filter \
  'git rm --cached --ignore-unmatch path/to/file.py' \
  --prune-empty --tag-name-filter cat -- --all

# Force push (if remote)
git push origin --force --all
```

### Step 3: Add to .gitignore
```bash
echo "config/secrets.py" >> .gitignore
git add .gitignore
git commit -m "security: prevent secrets in git"
```

## Best Practices

### 1. Use Environment Variables
```python
import os
from functools import lru_cache

@lru_cache
def get_settings():
    return Settings()

settings = get_settings()
```

### 2. Separate Config Files
```
project/
├── config/
│   ├── settings.py          # Settings class
│   ├── production.py        # Prod config (no secrets!)
│   └── development.py       # Dev config (no secrets!)
├── .env                     # Secrets (gitignored!)
└── .env.example             # Template (committed)
```

### 3. Use Secret Management
```python
# For production, use secret managers
from google.cloud import secretmanager

def get_secret(secret_id: str) -> str:
    """Fetch secret from Google Secret Manager."""
    client = secretmanager.SecretManagerServiceClient()
    name = f"projects/{PROJECT_ID}/secrets/{secret_id}/versions/latest"
    response = client.access_secret_version(request={"name": name})
    return response.payload.data.decode("UTF-8")
```

### 4. Docker Secrets
```yaml
# docker-compose.yml
services:
  app:
    secrets:
      - db_password
      - api_key

secrets:
  db_password:
    file: ./secrets/db_password.txt
  api_key:
    file: ./secrets/api_key.txt
```

## False Positives

If scanner blocks legitimate code:

### Option 1: Use different variable name
```python
# Instead of
API_KEY_EXAMPLE = "sk-test-example"  # Blocked

# Use
EXAMPLE_API_KEY_FORMAT = "sk-test-xxx"  # May pass
```

### Option 2: Comment explanation
```python
# Example key format for documentation (not real)
# Scanner: ignore-secret
API_KEY_FORMAT = "sk-live-xxxxxxxxxxxx"
```

### Option 3: Move to documentation
```markdown
<!-- README.md -->
API keys should follow format: `sk-live-xxxxxxxxxxxx`
```

## Integration with Git Hooks

Add to `.git/hooks/pre-commit`:
```bash
#!/bin/bash

echo "🔍 Scanning for secrets..."

# Run secret scanner
if git diff --cached --name-only | xargs grep -nHE '(API_KEY|SECRET|PASSWORD|TOKEN)\s*=\s*["'\''][^"'\'']{8,}'; then
    echo ""
    echo "❌ Potential secrets detected in staged files!"
    echo "Please remove hardcoded secrets and use environment variables."
    echo ""
    echo "Quick fix:"
    echo "  1. Move secret to .env file"
    echo "  2. Use os.getenv('SECRET_NAME') in code"
    echo "  3. Stage changes and retry commit"
    exit 1
fi

echo "✅ No secrets detected"
exit 0
```

## Monitoring and Alerts

Set up monitoring for secret exposure:

```python
# Use Sentry to track potential secret leaks
import sentry_sdk

def check_for_secrets_in_logs(log_message: str) -> bool:
    """Check if log message contains potential secrets."""
    patterns = [
        r'sk-[a-zA-Z0-9]{20,}',  # OpenAI keys
        r'AKIA[0-9A-Z]{16}',     # AWS keys
        r'ghp_[a-zA-Z0-9]{36}',  # GitHub tokens
    ]
    for pattern in patterns:
        if re.search(pattern, log_message):
            sentry_sdk.capture_message(
                "Potential secret in logs",
                level="warning",
            )
            return True
    return False
```

## Remember

**Once a secret is committed, consider it compromised.**

Always:
- ✅ Rotate compromised secrets immediately
- ✅ Use environment variables
- ✅ Keep .env in .gitignore
- ✅ Use secret managers in production
- ✅ Scan before every commit

Never:
- ❌ Commit secrets to git
- ❌ Share secrets in Slack/email
- ❌ Reuse secrets across environments
- ❌ Store secrets in code comments
- ❌ Log secret values