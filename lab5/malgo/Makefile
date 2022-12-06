export GOOS = linux
export GOARCH = amd64
export CGO_ENABLED = 1
export CC = $(shell which musl-gcc || echo gcc)

PACKAGE := malgo
PACKAGE_VERSION ?= dev
PROJECT := driver
OUTFILE := $(PROJECT)
BUILD_DIR ?= .
BASE_DOMAIN ?= "localhost"
TIMESTAMP := $(shell date -R)

LDFLAGS := -X '${PACKAGE}/core.BaseDomain=${BASE_DOMAIN}'
LDFLAGS += -X '${PACKAGE}/core.ProjectName=${PROJECT}'
LDFLAGS += -X '${PACKAGE}/core.ProjectVersion=${PACKAGE_VERSION}'
LDFLAGS += -X '${PACKAGE}/core.BuildTime=${TIMESTAMP}'
LDFLAGS += -linkmode external
LDFLAGS += -extldflags '-static -fno-PIC'

default:
	go build -ldflags="${LDFLAGS}" -o "${BUILD_DIR}/${OUTFILE}"

release: default
	strip "${BUILD_DIR}/${OUTFILE}" -o "${BUILD_DIR}/${OUTFILE}.release"
	upx "${BUILD_DIR}/${OUTFILE}.release"

clean:
	rm -f "${BUILD_DIR}/*"
