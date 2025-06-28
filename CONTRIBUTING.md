# Contributing to webview-proc

Thank you for your interest in contributing to `webview-proc`! This package simplifies running `pywebview` windows in a separate thread, and we welcome contributions to improve its functionality, stability, and usability. Below are guidelines to help you contribute effectively.

## Code of Conduct
By participating, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please treat everyone with respect and foster a welcoming community.

## Getting Started
1. **Fork the Repository**: Fork the `webview-proc` repository on GitHub and clone your fork locally.
   ```bash
   git clone https://github.com/your-username/webview-proc.git
   cd webview-proc
   ```
2. **Set Up the Environment**: Install dependencies using pip:
   ```bash
   pip install -e ".[dev]"
   ```
   Required: `pywebview`. Optional: `pytest`, `black`, `flake8`, `mypy` for development.
3. **Create a Branch**: Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines
- **Code Style**: Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) and use [Black](https://black.readthedocs.io/) for formatting. Run `black .` before committing.
- **Linting**: Use [Flake8](https://flake8.pycqa.org/) to ensure code quality. Run `flake8 .` to check for issues.
- **Type Hints**: Use type hints (per [PEP 484](https://www.python.org/dev/peps/pep-484/)) and verify with `mypy`.
- **Testing**: Write tests using [pytest](https://docs.pytest.org/). Ensure all tests pass with `pytest .`. Tests should cover cross-platform behavior (Windows, macOS, Linux) and `pywebview` backends (Qt, GTK, Cocoa).
- **Documentation**: Update docstrings and the `README.md` for any new features or changes. Use [Google-style docstrings](https://google.github.io/styleguide/pyguide.html).

## Submitting a Pull Request
1. **Commit Changes**: Write clear, concise commit messages. Group related changes logically.
   ```bash
   git commit -m "Add feature X to WebViewProcess"
   ```
2. **Push to Your Fork**: Push your branch to your forked repository.
   ```bash
   git push origin feature/your-feature-name
   ```
3. **Open a Pull Request**: Go to the `webview-proc` repository on GitHub and open a pull request from your branch. Include:
   - A clear title (e.g., "Add support for custom webview backends").
   - A description of the changes, why they’re needed, and how they were tested.
   - Reference any related issues (e.g., "Fixes #123").
4. **Code Review**: Respond to feedback from maintainers. Ensure all CI checks (e.g., tests, linting) pass.

## Types of Contributions
- **Bug Fixes**: Fix issues with `WebViewProcess` functionality, such as window operations or thread safety.
- **Features**: Add new window operations or support for other webview backends (e.g., QtWebEngine, CEF).
- **Tests**: Improve test coverage, especially for cross-platform scenarios.
- **Documentation**: Enhance `README.md`, docstrings, or add examples for different use cases.
- **Performance**: Optimize thread communication or window operation performance.

## Reporting Issues
- Use the [Issue Tracker](https://github.com/username/webview-proc/issues) to report bugs or suggest features.
- Provide a clear description, steps to reproduce, platform details (e.g., OS, `pywebview` backend), and any error messages.

## Community
Join discussions in the [Issue Tracker](https://github.com/username/webview-proc/issues) or contact maintainers for questions. We appreciate your contributions to making `webview-proc` better!