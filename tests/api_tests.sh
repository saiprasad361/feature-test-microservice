#!/bin/bash
set -e

SERVICE_URL=$1

echo "Running API tests on $SERVICE_URL"

echo "Checking health endpoint..."
curl -s "$SERVICE_URL/health" | grep UP

echo "Checking feature version..."
curl -s "$SERVICE_URL/version" | grep v2-feature-enabled

echo "Checking bugfix endpoint..."
curl -s "$SERVICE_URL/bugfix" | grep "Bug fixed successfully"

echo "All tests passed ✅"

