#!/bin/bash -eu

python3 -m pip install \
  --disable-pip-version-check \
  --no-cache-dir \
  --no-deps \
  --only-binary=:all: \
  --require-hashes \
  --requirement "${SRC}/hermes-tweet/.clusterfuzzlite/requirements.txt"

for fuzzer in "${SRC}"/hermes-tweet/fuzz/*_fuzzer.py; do
  fuzzer_name="$(basename -s .py "${fuzzer}")"
  fuzzer_package="${fuzzer_name}.pkg"

  pyinstaller \
    --add-data "${SRC}/hermes-tweet/hermes_tweet/catalog_data.json:hermes_tweet" \
    --distpath "${OUT}" \
    --onefile \
    --name "${fuzzer_package}" \
    --paths "${SRC}/hermes-tweet" \
    "${fuzzer}"

  cat >"${OUT}/${fuzzer_name}" <<EOF
#!/bin/sh
# LLVMFuzzerTestOneInput
this_dir=\$(dirname "\$0")
exec "\${this_dir}/${fuzzer_package}" "\$@"
EOF
  chmod +x "${OUT}/${fuzzer_name}"
done
