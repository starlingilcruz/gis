set -e

# skip completed coverage
# pytest --cov=.. --cov-report=term-missing:skip-covered --cov-report=xml

pytest --cov --cov-report=xml --no-cov
