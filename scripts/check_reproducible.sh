#!/usr/bin/env bash

# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

set -euo pipefail

cd "$(dirname "$0")/.."

reproducibility_workspace="$(
  mktemp -d "${TMPDIR:-/tmp}/hermes-tweet-reproducibility.XXXXXX"
)"
trap 'rm -rf -- "$reproducibility_workspace"' EXIT

mkdir "$reproducibility_workspace/first" "$reproducibility_workspace/second"

echo "==> Building distributions twice"
SOURCE_DATE_EPOCH=946684800 \
  uv run python -m build --outdir "$reproducibility_workspace/first"
SOURCE_DATE_EPOCH=946684800 \
  uv run python -m build --outdir "$reproducibility_workspace/second"

first_archives=("$reproducibility_workspace"/first/*)
if [[ "${#first_archives[@]}" -ne 2 ]]; then
  echo "Expected one wheel and one source archive." >&2
  exit 1
fi

for first_archive in "${first_archives[@]}"; do
  archive_name="${first_archive##*/}"
  second_archive="$reproducibility_workspace/second/$archive_name"
  if [[ ! -f "$second_archive" ]]; then
    echo "Second build omitted $archive_name." >&2
    exit 1
  fi

  cmp "$first_archive" "$second_archive"

  if [[ "$archive_name" == *.whl ]]; then
    archive_listing="$(unzip -Z1 "$first_archive")"
    expected_license="/licenses/LICENSE"
    expected_wheel_members=(
      "hermes_tweet/plugin.yaml"
      "hermes_tweet/catalog_data.json"
      "hermes_tweet/skills/hermes-tweet/SKILL.md"
      "hermes_tweet/skills/hermes-tweet/skill-card.md"
      "hermes_tweet/skills/hermes-tweet/references/endpoint-contract.md"
    )
    for expected_member in "${expected_wheel_members[@]}"; do
      if ! grep -Fqx "$expected_member" <<<"$archive_listing"; then
        echo "$archive_name omits $expected_member." >&2
        exit 1
      fi
    done
  elif [[ "$archive_name" == *.tar.gz ]]; then
    archive_listing="$(tar -tzf "$first_archive")"
    expected_license="/LICENSE"
    if [[ "$archive_listing" != *"/scripts/check_reproducible.sh"* ]]; then
      echo "$archive_name omits its reproducibility verifier." >&2
      exit 1
    fi
  else
    echo "Unexpected distribution type: $archive_name." >&2
    exit 1
  fi

  if [[ "$archive_listing" != *"$expected_license"* ]]; then
    echo "$archive_name omits its MIT license." >&2
    exit 1
  fi
done

echo "Hermes Tweet wheel and source archives are reproducible."
