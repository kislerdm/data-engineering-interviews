#!/bin/sh

DIR="$( cd "$(dirname "${0}")/../.." >/dev/null 2>&1 ; pwd -P )"

export DIR_SOURCE_QUESTIONS=${DIR}/questions
export DIR_SITE_CONTENT=${DIR}/website/content

export DIR_SOURCE_IMG=${DIR}/img
export DIR_DESTINATION_IMG=${DIR}/website/static/img

export PATH_COC=${DIR}/CODE-OF-CONDUCT.md