# Contributing to Alchemyst LangChain

Thank you for your interest in contributing! This project uses an automated CI/CD pipeline to manage testing, versioning, and deployments.

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Git

### Development Setup

1. **Fork and clone the repository**
```bash
   git clone https://github.com/YOUR_USERNAME/alchemyst-langchain.git
   cd alchemyst-langchain
```

2. **Create a virtual environment**
```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install in development mode**
```bash
   pip install -e ".[dev]"
```

4. **Set up environment variables**
```bash
   cp .env.example .env
   # Edit .env and add your ALCHEMYST_AI_API_KEY
```

---

## 📝 Development Workflow

### 1. Create a Branch
```bash
git checkout -b feat/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Format and Lint

We use Ruff for lightning-fast linting and formatting. Run these before committing to ensure the CI passes:
```bash
# Format code
ruff format src/

# Lint and auto-fix issues
ruff check --fix src/
```

### 3. Run Tests

Ensure all tests pass locally using pytest:
```bash
# Run all tests with coverage
pytest -v --cov=alchemyst_langchain
```

### 4. Commit Your Changes (Important)

We use **Conventional Commits**. This is required because our CI/CD uses these tags to automatically calculate the next version number and update the CHANGELOG.

**Format:** `<type>: <description>`

| Type | Description | Resulting Version Bump |
|------|-------------|------------------------|
| `feat` | A new feature | Minor (e.g., 0.1.0 → 0.2.0) |
| `fix` | A bug fix | Patch (e.g., 0.1.0 → 0.1.1) |
| `perf` | Performance improvement | Patch |
| `docs` | Documentation only | None (CI only) |
| `feat!` | Breaking change | Major (e.g., 0.1.0 → 1.0.0) |

**Example:**
```bash
git commit -m "feat: add support for semantic session search"
```

---

## 📦 Automated Release Process

Once your Pull Request is merged into the `main` branch, the following happens automatically:

1. GitHub Actions runs the test matrix across Python 3.10, 3.11, and 3.12.
2. Python Semantic Release analyzes your commit tags.
3. The version is bumped in `pyproject.toml` and `src/alchemyst_langchain/__init__.py`.
4. A new GitHub Release is created and the package is published to PyPI.

---

## 🧪 Testing Guidelines

- Place new tests in the `tests/` directory.
- Use descriptive test names (e.g., `test_memory_clears_on_session_end`).
- Test for both success cases and edge cases (empty inputs, invalid keys).

---

## 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/Alchemyst-ai/alchemyst-langchain/issues)
- **Documentation**: [getalchemystai.com/docs](https://getalchemystai.com/docs)

---

Thank you for helping us grow the Alchemyst ecosystem! 🎉