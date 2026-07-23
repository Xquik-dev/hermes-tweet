# SPDX-FileCopyrightText: 2026 Xquik Contributors
# SPDX-License-Identifier: MIT

FROM gcr.io/oss-fuzz-base/base-builder-python@sha256:d4ef5a787f3e1a420721da74823202185dc04e2e792984671c31a67d7ce66832

COPY . ${SRC}/hermes-tweet
WORKDIR ${SRC}/hermes-tweet
COPY .clusterfuzzlite/build.sh ${SRC}/build.sh

# This image builds fuzzers and exits. It never serves health-checkable traffic.
HEALTHCHECK NONE
