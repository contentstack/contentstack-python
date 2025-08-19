#!/usr/bin/env bash
"""
Talisman secrets detection hook for Husky-style pre-commit setup.
This hook runs Talisman to detect potential secrets in commits.
"""

# Check if Talisman is available
if ! command -v talisman &> /dev/null; then
    echo "❌ Talisman not found. Please install it first:"
    echo "   # macOS"
    echo "   brew install talisman"
    echo "   # Linux"
    echo "   curl -sL https://github.com/thoughtworks/talisman/releases/latest/download/talisman_linux_amd64 -o talisman"
    echo "   chmod +x talisman"
    echo "   sudo mv talisman /usr/local/bin/"
    exit 1
fi

echo "🔐 Running Talisman secrets detection..."

# Run Talisman with pre-commit hook
if talisman --githook pre-commit; then
    echo "✅ Talisman check passed - no secrets detected"
    exit 0
else
    echo "❌ Talisman found potential secrets in your changes"
    echo ""
    echo "💡 To fix this:"
    echo "1. Review the files mentioned above"
    echo "2. Remove any actual secrets from your code"
    echo "3. If the file contains legitimate test data, add it to .talismanrc:"
    echo "   talisman --checksum path/to/file"
    echo "   # Then add the checksum to .talismanrc"
    exit 1
fi
