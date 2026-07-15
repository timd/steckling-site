#!/bin/sh
# steckling.dev/install.sh — thin wrapper so the short one-liner works:
#
#   curl -fsSL steckling.dev/install.sh | sh
#
# The canonical installer lives in the main repo and is fetched at run time,
# so this file never needs a version bump.
set -e
exec sh -c "$(curl -fsSL https://raw.githubusercontent.com/timd/steckling/main/install.sh)"
