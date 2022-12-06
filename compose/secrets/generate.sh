#!/bin/bash

set -euo pipefail

generate_flag() {
    echo "flag{$1:$2}"
}

main() {
    BASE_DIR="$1"
    KEYFILE="${BASE_DIR}/key"

    mkdir -p "${BASE_DIR}"
    mkdir -p "${BASE_DIR}/pass"
    mkdir -p "${BASE_DIR}/flags"
    mkdir -p "${BASE_DIR}/misc"

    # Generate IKM
    if [ ! -f "${KEYFILE}" ]; then
        python3 flaggen.py generate_key > "${KEYFILE}"
    fi

    KEYARG="-k ${KEYFILE}"
    CMD="python3 flaggen.py domain ${KEYARG}"

    # Generate secrets
    ${CMD} secrets:POSTGRES_PASSWORD > "${BASE_DIR}/pass/POSTGRES_PASSWORD"
    ${CMD} secrets:POSTGRES_WEB_PASSWORD > "${BASE_DIR}/pass/POSTGRES_WEB_PASSWORD"
    #${CMD} secrets:MINIO_ROOT_PASSWORD > "${BASE_DIR}/pass/MINIO_ROOT_PASSWORD"
    echo "Fall2022password123!" > "${BASE_DIR}/pass/MINIO_ROOT_PASSWORD"
    ${CMD} secrets:STAFF_PASSWORD > "${BASE_DIR}/pass/STAFF_PASSWORD"

    # Generate flags
    generate_flag sqli $(${CMD} flags:sqli) > "${BASE_DIR}/flags/SQLI"
    generate_flag csrf $(${CMD} flags:csrf) > "${BASE_DIR}/flags/CSRF"
    generate_flag rce $(${CMD} flags:rce) > "${BASE_DIR}/flags/RCE"
    generate_flag xss $(${CMD} flags:xss) > "${BASE_DIR}/flags/XSS"
    generate_flag users $(${CMD} flags:users) > "${BASE_DIR}/flags/USERS"
    generate_flag wildcard:vhost $(${CMD} flags:wildcard.subdomain) > "${BASE_DIR}/flags/WILDCARD_SUBDOMAIN"
    generate_flag wildcard:page $(${CMD} flags:wildcard.page_enumeration) > "${BASE_DIR}/flags/WILDCARD_PAGE_ENUMERATION"
    generate_flag wildcard:port $(${CMD} flags:wildcard.port_enumeration) > "${BASE_DIR}/flags/WILDCARD_PORT_ENUMERATION"
    generate_flag wildcard:scm $(${CMD} flags:wildcard.source_control) > "${BASE_DIR}/flags/WILDCARD_SOURCE_CONTROL"

    # Miscellaneous other secrets
    python3 flaggen.py word ${KEYARG} misc:SECRET_SUBDOMAIN ./wordlists/subdomains.txt \
        > "${BASE_DIR}/misc/SECRET_SUBDOMAIN"
    python3 flaggen.py word ${KEYARG} misc:SECRET_PAGE ./wordlists/common.txt \
        > "${BASE_DIR}/misc/SECRET_PAGE"
}

init() {
    if [ ! $# -eq 1 ]; then
        echo "Usage: $0 OUTPUT_DIRECTORY"
        exit 1
    fi

    main "$1"
}

init $@
