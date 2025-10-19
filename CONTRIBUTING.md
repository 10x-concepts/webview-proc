# Contributing to webview-proc

Thank you for your interest in contributing to `webview-proc`! This package simplifies running `pywebview` windows in a separate thread, and we welcome contributions to improve its functionality, stability, and usability. Below are guidelines to help you contribute effectively.

## Code of Conduct
By participating, you agree to abide by our [Code of Conduct](CODE_OF_CONDUCT.md). Please treat everyone with respect and foster a welcoming community.

## Getting Started
1. **Fork the Repository**: Fork the `webview-proc` repository on GitHub and clone your fork locally.
   ```bash
   git clone https://github.com/your_user_name/webview-proc.git
   cd webview-proc
   ```
2. **Set Up the Environment**: Install dependencies using uv:
   ```bash
   uv sync --all-extras
   ```
3. **Create a Branch**: Create a new branch for your changes:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Development Guidelines
- **Code Style & Linting**: Use [Ruff](https://docs.astral.sh/ruff/) for formatting, linting, and type checking. Run `ruff check .` to lint and check types, and `ruff format .` to auto-format your code.
- **Testing**: Write tests using [pytest](https://docs.pytest.org/). Ensure all tests pass with `pytest .`. Tests should cover cross-platform behavior (Windows, macOS, Linux) and `pywebview` backends (Qt, GTK, Cocoa).
- **Documentation**: Update docstrings and the `README.md` for any new features or changes.

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
- Use the [Issue Tracker](https://github.com/10x-concepts/webview-proc/issues) to report bugs or suggest features.
- Provide a clear description, steps to reproduce, platform details (e.g., OS, `pywebview` backend), and any error messages.

## Community
Join our community on [Discord](https://discord.gg/Cmw45JPJZ5) for discussion, support, and collaboration.