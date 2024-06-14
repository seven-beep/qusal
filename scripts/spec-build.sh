#!/bin/sh

## SPDX-FileCopyrightText: 2023 - 2024 Benjamin Grande M. S. <ben.grande.b@gmail.com>
##
## SPDX-License-Identifier: AGPL-3.0-or-later

set -eu

usage(){
  echo "Usage: ${0##*/} PROJECT [PROJECT ...]" >&2
  exit 1
}

build_rpm(){
  counter=$((counter+1))
  project="${1}"
  group="$(${spec_get} "${project}" group)"
  version="$(${spec_get} "${project}" version)"
  license_csv="$(${spec_get} "${project}" license_csv)"
  spec="rpm_spec/${group}-${project}.spec"

  "${spec_gen}" "${project}"

  ## All specs have the same format, only lint the first one.
  if test "${counter}" = "1"; then
    rpmlint "${spec}"
  fi

  if grep -q "^BuildRequires: " "${spec}"; then
    sudo dnf build-dep "${spec}"
  fi

  mkdir -p \
    "${build_dir}/BUILD/${group}-${project}/LICENSES/" \
    "${build_dir}/SOURCES/${group}-${project}/LICENSES"

  cp -r "salt/${project}/"* "${build_dir}/BUILD/${group}-${project}/"
  cp -r "salt/${project}/"* "${build_dir}/SOURCES/${group}-${project}/"
  for license in $(echo "${license_csv}" | tr "," " "); do
    license_dir="LICENSES"
    if test -d "salt/${project}/LICENSES"; then
      license_dir="salt/${project}/LICENSES"
    fi
    cp "${license_dir}/${license}.txt" "${build_dir}/BUILD/${group}-${project}/LICENSES/"
  done

  ## TODO: use qubes-builderv2 with mock or qubes executor
  rpmbuild -ba --quiet --clean -- "${spec}"
  if test -n "${key_id}"; then
    rpm_basename="${build_dir}/RPMS/noarch/${group}-${project}-${version}-"
    rpm_suffix=".noarch.rpm"
    ## TODO: target only the latest release
    rpmsign --key-id="${key_id}" --digest-algo=sha512 --addsign \
      -- "${rpm_basename}"*"${rpm_suffix}" </dev/null
    gpg="$(git config --get gpg.program)" || gpg="gpg"
    dbpath="$(mktemp -d)"
    trap 'rm -rf -- "${dbpath}"' EXIT INT HUP QUIT ABRT
    tmp_file="${dbpath}/${key_id}.asc"
    "${gpg}" --export --armor "${key_id}" | tee "${tmp_file}" >/dev/null
    rpmkeys --dbpath="${dbpath}" --import "${tmp_file}"
    ## TODO: target only the latest relase
    rpmkeys --dbpath="${dbpath}" --checksig --verbose \
      -- "${rpm_basename}"*"${rpm_suffix}"
  fi
}

case "${1-}" in
  -h|--?help) usage;;
esac

command -v git >/dev/null || { echo "Missing program: git" >&2; exit 1; }
cd "$(git rev-parse --show-toplevel)" || exit 1
./scripts/requires-program.sh dnf rpmlint rpmbuild rpmsign
build_dir="${HOME}/rpmbuild"

if command -v rpmdev-setuptree >/dev/null; then
  rpmdev-setuptree
else
  mkdir -p \
    "${build_dir}/BUILD" "${build_dir}/BUILDROOT" "${build_dir}/RPMS" \
    "${build_dir}/SOURCES" "${build_dir}/SPECS" "${build_dir}/SRPMS"
fi

key_id="$(git config --get user.signingKey)" || true
spec_gen="./scripts/spec-gen.sh"
spec_get="./scripts/spec-get.sh"

if test -z "${1-}"; then
  # shellcheck disable=SC2046
  set -- $(find salt/ -mindepth 1 -maxdepth 1 -type d -printf '%f\n' \
           | sort -d | tr "\n" " ")
fi
counter=0
for p in "$@"; do
  build_rpm "${p}"
done
