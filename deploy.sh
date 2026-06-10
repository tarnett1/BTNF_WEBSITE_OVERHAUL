#!/bin/bash

# Ensure we're in the repository directory
cd "$(dirname "$0")"


# Check if there are any changes
if [ -z "$(git status --porcelain)" ]; then
  echo "No changes detected. Working directory is clean."
  exit 0
fi

# Ask for a commit message or use a default one
read -p "Enter commit message (default: 'Update website assets'): " msg
if [ -z "$msg" ]; then
  msg="Update website assets"
fi

# Stage all changes
echo "Staging changes..."
git add .

# Commit changes
echo "Committing changes..."
git commit -m "$msg"

# Push to GitHub
echo "Pushing to GitHub..."
git push origin main

if [ $? -eq 0 ]; then
  echo "✅ Changes successfully pushed to GitHub!"
  echo "🚀 Your CI/CD pipeline is running. Your website will be live in a few seconds."
  echo "🔗 View deployment: https://tarnett1.github.io/BTNF_WEBSITE_OVERHAUL/"
else
  echo "❌ Error: Failed to push to GitHub. Please check your internet connection or credentials."
fi















