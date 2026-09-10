#!/usr/bin/env bash
set -euo pipefail
ROOT="${GITHUB_WORKSPACE:-$(pwd)}"
exec bash "$ROOT/q041_prepare_frozen_core_v15.sh" "$@"
