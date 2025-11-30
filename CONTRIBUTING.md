# Contributing to Bill Subscription Tracker

Thanks for your interest in contributing! This guide will help you get started.

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/bill-subscription-tracker.git
   cd bill-subscription-tracker
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -r backend/requirements.txt
   ```

## Development Workflow

### Code Style
- Follow PEP 8
- Use type hints for all functions
- Add docstrings to all modules, classes, and functions
- Maximum line length: 100 characters

### Testing
```bash
# Run all tests
pytest -v

# Run with coverage
pytest --cov=backend

# Run specific test
pytest backend/test_api.py::test_health_check
```

### Before Submitting a PR
1. **Run tests**: Ensure all tests pass
2. **Add tests**: Any new feature must have tests
3. **Update docs**: Document your changes
4. **Follow style guide**: Use black for formatting

## Pull Request Process

1. Create a feature branch: `git checkout -b feature/your-feature`
2. Make changes and commit: `git commit -m "Add feature"`
3. Push: `git push origin feature/your-feature`
4. Create PR with clear description
5. Address review comments
6. Merge when approved

## Reporting Issues

Use GitHub Issues with:
- **Bug**: Describe the bug and steps to reproduce
- **Feature**: Explain the use case and benefits
- **Documentation**: Point out unclear sections

## Code of Conduct

Be respectful, inclusive, and professional. We welcome all contributions!
