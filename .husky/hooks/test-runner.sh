#!/usr/bin/env bash
"""
Test runner hook for Husky-style pre-push setup.
This hook runs tests and coverage checks before pushing.
"""

echo "🧪 Running tests and coverage checks..."

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if pytest is available
if ! command_exists pytest; then
    echo "❌ pytest not found. Please install it first:"
    echo "   pip install pytest pytest-cov"
    exit 1
fi

# Run tests
echo "  - Running tests..."
if pytest --html=tests/report/test-report.html; then
    echo "    ✅ All tests passed"
else
    echo "    ❌ Tests failed. Please fix before pushing."
    exit 1
fi

# Run coverage check
echo "  - Checking test coverage..."
if command_exists pytest; then
    if pytest --cov=contentstack --cov-report=term-missing; then
        echo "    ✅ Coverage check completed"
    else
        echo "    ❌ Coverage check failed. Please improve test coverage."
        exit 1
    fi
else
    echo "    ⚠️  pytest-cov not installed, skipping coverage check"
    echo "    💡 Install with: pip install pytest-cov"
fi

echo "✅ All test checks passed!"
