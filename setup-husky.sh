#!/bin/sh

# Set up husky
yarn add husky --dev

# Create .husky directory if it doesn't exist
mkdir -p .husky/_

# Make hooks executable
chmod +x .husky/pre-commit
chmod +x .husky/_/husky.sh

# Initialize git hooks
npx husky install

echo "Husky pre-commit hooks set up successfully!" 