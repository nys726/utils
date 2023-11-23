#!/bin/bash

OS=$(uname -s)
DIR="steeltools"
CURRENT_DIR=$PWD
MATCH_VERSION=$1
REPLACE_VERSION=$2
COMMIT_MSG=$3

TARGET_FILES=("setup.py" "$DIR/__init__.py")

show_help() {
    echo "이 스크립트의 도움말을 표시합니다."
    echo "사용법: version_up.sh [ 현재 버전] [업데이트 버전]"
    echo "예  시: version_up.sh 0.0.1 0.0.2"
    echo
    echo "옵션:"
    echo "  -h, --help  도움말 표시"
}

# 옵션 처리
if [[ $1 == "-h" || $1 == "--help" ]]; then
    show_help
    exit 0
fi

if [ -z "$1" ]; then
    echo "현재 버전이 입력 되지 않았습니다."
    show_help
    exit 1
elif [ -z "$2" ]; then
    echo "업데이트 버전이 입력 되지 않았습니다."
    show_help
    exit 1
fi


for file in "${TARGET_FILES[@]}"; do
    if [ "$OS" == "Darwin" ]; then
        sed -i "" "s/$MATCH_VERSION/$REPLACE_VERSION/g" "$CURRENT_DIR/$file"
    elif [ "$OS" == "Linux" ]; then
        sed -i "s/$MATCH_VERSION/$REPLACE_VERSION/g" "$CURRENT_DIR/$file"
    fi
done

`git add setup.py ${DIR}/__init__.py`
echo "git add"
`git commit -m Bump Up Version: ${COMMIT_MSG}`
echo "git commit"
`git push`
echo "git push"
`git tag -a v${REPLACE_VERSION} -m Bump UP Version: ${COMMIT_MSG}`
echo "git tag commit"
`git push origin v${REPLACE_VERSION}`
