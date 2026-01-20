# Contributing to Alchemyst LangChain

Thank you for your interest in contributing! We welcome contributions from the community.

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- Git
- Virtual environment tool (venv, conda, etc.)

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
   # Edit .env and add your API keys
   ```

5. **Run tests to verify setup**

   ```bash
   pytest
   ```

## 📝 Development Workflow

### 1. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/bug-description
```

### 2. Make Your Changes

- Write clean, readable code
- Follow existing code style
- Add tests for new features
- Update documentation as needed

### 3. Run Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=alchemyst_langchain

# Run specific test
pytest tests/integration/test_memory.py::TestMemoryBasics
```

### 4. Format and Lint

```bash
# To format and sort imports (if you have formatters installed)
ruff format src/ && ruff check --select I --fix src/

# for linting checks run
ruff check src/

#To confirm everything is correct
ruff format --check src/ && ruff check src/
```

### 5. Commit Your Changes

```bash
git add .
git commit -m "feat: Add new feature description"
```

**Commit Message Format:**

```
<type>: <description>

[optional body]

[optional footer]
```

**Types:**
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `test`: Adding or updating tests
- `refactor`: Code refactoring
- `chore`: Maintenance tasks
- `perf`: Performance improvements

**Examples:**

```bash
git commit -m "feat: Add async support to AlchemystMemory"
git commit -m "fix: Handle empty session IDs correctly"
git commit -m "docs: Update README with new examples"
```

### 6. Push and Create PR

```bash
git push origin feature/your-feature-name
```

Then go to GitHub and create a Pull Request.

## 🧪 Testing Guidelines

### Writing Tests

- Place tests in `tests/integration/`
- Use descriptive test names: `test_memory_saves_context_successfully`
- Test both success and failure cases
- Use real API calls (no mocks) for integration tests

### Test Structure

```python
def test_feature_description(memory):
    """Test that feature works as expected."""
    # Arrange
    inputs = {"input": "test"}
    
    # Act
    result = memory.some_method(inputs)
    
    # Assert
    assert result is not None
    assert "expected" in result
```

### Running Tests

```bash
# All tests
pytest

# Specific file
pytest tests/integration/test_memory.py

# Specific test
pytest tests/integration/test_memory.py::test_name

# With output
pytest -v

# Stop on first failure
pytest -x
```

## 📚 Documentation

### Code Documentation

- Add docstrings to all public functions and classes
- Use Google-style docstrings

```python
def function_name(param1: str, param2: int) -> bool:
    """Brief description of function.
    
    Longer description if needed.
    
    Args:
        param1: Description of param1
        param2: Description of param2
        
    Returns:
        Description of return value
        
    Raises:
        ValueError: When parameter is invalid
    """
    pass
```

### README Updates

Update README.md if you:
- Add new features
- Change API
- Add new examples
- Update installation process

## 🐛 Reporting Bugs

### Before Submitting

1. Check existing issues
2. Verify bug with latest version
3. Collect relevant information

### Bug Report Template

```markdown
**Description**
Clear description of the bug

**To Reproduce**
Steps to reproduce:
1. 
2. 
3. 

**Expected Behavior**
What should happen

**Actual Behavior**
What actually happens

**Environment**
- OS: [e.g. macOS 14.0]
- Python version: [e.g. 3.11]
- Package version: [e.g. 0.1.0]

**Additional Context**
Any other relevant information
```

## 💡 Feature Requests

We welcome feature requests! Please:

1. Check if feature already exists or is planned
2. Describe the use case clearly
3. Explain why this would be useful
4. Provide examples if possible

## 🔍 Code Review Process

### What We Look For

- ✅ Code quality and style
- ✅ Test coverage
- ✅ Documentation
- ✅ No breaking changes (or clearly marked)
- ✅ Commit message quality

### PR Checklist

Before submitting, ensure:

- [ ] Tests pass (`pytest`)
- [ ] Code is formatted
- [ ] Documentation updated
- [ ] CHANGELOG.md updated (for significant changes)
- [ ] Commit messages follow convention
- [ ] No merge conflicts
- [ ] PR description is clear

## 📋 Pull Request Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Changes Made
- Change 1
- Change 2
- Change 3

## Testing
- [ ] Tests added/updated
- [ ] All tests pass
- [ ] Manual testing completed

## Documentation
- [ ] README updated
- [ ] Docstrings added/updated
- [ ] Examples added/updated

## Checklist
- [ ] Code follows project style
- [ ] Self-review completed
- [ ] Comments added for complex code
- [ ] No new warnings
- [ ] CHANGELOG.md updated (if needed)
```

## 🎯 Coding Standards

### Python Style

- Follow PEP 8
- Use type hints
- Maximum line length: 88 characters (Black default)
- Use descriptive variable names

### Good Practices

```python
# ✅ Good
def save_user_context(user_id: str, context: Dict[str, Any]) -> bool:
    """Save context for a specific user."""
    if not user_id:
        raise ValueError("user_id cannot be empty")
    # ... implementation

# ❌ Avoid
def save(u, c):
    # ... implementation
```

### Imports

```python
# Standard library
import os
from typing import Dict, Any

# Third party
from langchain.memory import BaseChatMemory

# Local
from alchemyst_langchain.utils import helper_function
```

## 🤝 Code of Conduct

### Our Standards

- Be respectful and inclusive
- Welcome newcomers
- Accept constructive criticism
- Focus on what's best for the community

### Unacceptable Behavior

- Harassment or discrimination
- Trolling or insulting comments
- Publishing private information
- Other unprofessional conduct

## 📞 Getting Help

- **Issues**: [GitHub Issues](https://github.com/Alchemyst-ai/alchemyst-langchain/issues)
- **Email**: support@alchemyst.ai
- **Documentation**: [getalchemystai.com/docs](https://getalchemystai.com/docs)

## 📜 License

By contributing, you agree that your contributions will be licensed under the MIT License.

## 🙏 Recognition

Contributors will be recognized in:
- CHANGELOG.md
- GitHub contributors page
- Release notes (for significant contributions)

---

**Thank you for contributing to Alchemyst LangChain!** 🎉