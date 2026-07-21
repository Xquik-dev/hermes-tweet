#!/bin/bash -eu

python3 -m pip install .

for fuzzer in "${SRC}"/hermes-tweet/fuzz/*_fuzzer.py; do
  fuzzer_name="$(basename -s .py "${fuzzer}")"
  fuzzer_package="${fuzzer_name}.pkg"

  pyinstaller --distpath "${OUT}" --onefile --name "${fuzzer_package}" "${fuzzer}"

  cat >"${OUT}/${fuzzer_name}" <<EOF
#!/bin/sh
# LLVMFuzzerTestOneInput
this_dir=\$(dirname "\$0")
exec "\${this_dir}/${fuzzer_package}" "\$@"
EOF
  chmod +x "${OUT}/${fuzzer_name}"
done
