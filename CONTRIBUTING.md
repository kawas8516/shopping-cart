# Contributing to Shopping Cart Application

Thank you for your interest in contributing to the Shopping Cart Application! We welcome contributions from the community to help improve this project.

## How to Contribute

1. **Fork the Repository**: Click the "Fork" button on GitHub to create your own copy of the repository.

2. **Clone Your Fork**: Clone the forked repository to your local machine.
   ```
   git clone https://github.com/your-username/shopping-cart.git
   cd shopping-cart
   ```

3. **Create a Feature Branch**: Create a new branch for your feature or bug fix.
   ```
   git checkout -b feature/your-feature-name
   ```

4. **Make Your Changes**: Implement your feature or fix the bug.

5. **Test Your Changes**: Ensure your changes work correctly and don't break existing functionality.

6. **Commit Your Changes**: Commit your changes with a clear and descriptive commit message.
   ```
   git commit -am 'Add: brief description of your changes'
   ```

7. **Push to Your Branch**: Push your changes to your forked repository.
   ```
   git push origin feature/your-feature-name
   ```

8. **Create a Pull Request**: Go to the original repository and create a pull request from your branch.

## Development Setup

To set up the development environment:

1. Ensure you have Python 3.x installed.

2. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up the PostgreSQL database:
   - Install PostgreSQL
   - Create a database named 'shopping_cart'
   - Run the SQL commands in `postgresql_setup.sql`

4. Run the application:
   ```
   python main.py
   ```

## Coding Standards

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guide for Python code.
- Use descriptive and meaningful names for variables, functions, and classes.
- Add docstrings to functions and classes.
- Write clear and concise comments for complex logic.
- Keep functions small and focused on a single responsibility.

## Testing

- Write unit tests for new features and bug fixes.
- Run existing tests to ensure no regressions:
  ```
  python -m pytest
  ```
- Test the application manually to ensure UI functionality works correctly.

## Reporting Issues

If you find a bug or have a feature request:

1. Check the [GitHub Issues](https://github.com/kawas8516/shopping-cart/issues) to see if it's already reported.
2. If not, create a new issue with:
   - A clear title
   - Detailed description of the issue or feature
   - Steps to reproduce (for bugs)
   - Expected vs. actual behavior
   - Screenshots if applicable
   - Your environment (OS, Python version, etc.)

## Pull Request Guidelines

When submitting a pull request:

- Ensure your code follows the coding standards.
- Provide a clear description of what your changes do.
- Reference any related issues.
- Update documentation if necessary (README.md, docstrings, etc.).
- Make sure all tests pass.
- Keep pull requests focused on a single feature or fix.

## Code of Conduct

Please be respectful and constructive in all interactions. We aim to foster an inclusive and welcoming community.

## License

By contributing to this project, you agree that your contributions will be licensed under the same license as the project.