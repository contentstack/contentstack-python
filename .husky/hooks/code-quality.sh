#!/usr/bin/env bash
"""
Code quality checking hook for Husky-style pre-commit setup.
This hook runs Black, isort, flake8, and Bandit for code quality.
"""

echo "🐍 Running Python code quality checks..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check Black formatting
echo "  - Checking code formatting with Black..."
if command_exists black; then
    if black --check --diff .; then
        echo "    ✅ Black formatting check passed"
    else
        echo "    ❌ Black formatting issues found"
        echo "    💡 Run 'black .' to fix formatting"
        exit 1
    fi
else
    echo "    ⚠️  Black not installed, skipping formatting check"
    echo "    💡 Install with: pip install black"
fi

# Check isort import sorting
echo "  - Checking import sorting with isort..."
if command_exists isort; then
    if isort --check-only --diff .; then
        echo "    ✅ isort import sorting check passed"
    else
        echo "    ❌ isort import sorting issues found"
        echo "    💡 Run 'isort .' to fix import sorting"
        exit 1
    fi
else
    echo "    ⚠️  isort not installed, skipping import sorting check"
    echo "    💡 Install with: pip install isort"
fi

# Check flake8 linting
echo "  - Running linting with flake8..."
if command_exists flake8; then
    if flake8 --max-line-length=88 --extend-ignore=E203,W503 .; then
        echo "    ✅ flake8 linting check passed"
    else
        echo "    ❌ flake8 linting issues found"
        echo "    💡 Fix the linting issues above"
        exit 1
    fi
else
    echo "    ⚠️  flake8 not installed, skipping linting check"
    echo "    💡 Install with: pip install flake8"
fi

# Check Bandit security linting
echo "  - Running security linting with Bandit..."
if command_exists bandit; then
    if bandit -r . -f json -o bandit-report.json; then
        echo "    ✅ Bandit security linting check passed"
    else
        echo "    ❌ Bandit found security issues"
        echo "    💡 Review bandit-report.json for details"
        exit 1
    fi
else
    echo "    ⚠️  Bandit not installed, skipping security linting"
    echo "    💡 Install with: pip install bandit"
fi

echo "✅ All code quality checks passed!"
