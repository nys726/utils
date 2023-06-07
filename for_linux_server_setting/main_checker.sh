#!/bin/bash

missing_packages=""

check_install(){
    package_name=$1
    package_description=$2

    sudo apt-get install $package_name -y

    echo "$package_description가 성공적으로 설치되었습니다."
}

# Nvidia-docker 설치 확인
check_install_nvidia_docker() {
    package_name=$1
    package_description=$2

    distribution=$(. /etc/os-release;echo $ID$VERSION_ID) \
       && curl -s -L https://nvidia.github.io/nvidia-docker/gpgkey | sudo apt-key add - \
       && curl -s -L https://nvidia.github.io/nvidia-docker/$distribution/nvidia-docker.list | sudo tee /etc/apt/sources.list.d/nvidia-docker.list

    if ! command -v $package_description &> /dev/null; then
        echo "$package_description가 설치되어 있지 않습니다. 설치를 진행합니다."

        # 설치 명령어 (apt-get 사용)
        sudo apt-get update
        sudo apt-get install $package_name -y
        sudo systemctl restart docker

        # 설치 확인
        if ! command -v $package_description &> /dev/null; then
            echo "$package_description 설치에 실패했습니다."
            missing_packages+="$package_name "
        else
            echo "$package_description가 성공적으로 설치되었습니다."
        fi
    else
        echo "$package_description가 이미 설치되어 있습니다."
    fi
}

# 함수: 패키지 설치 확인 및 추가
check_install_package() {
    package_name=$1
    package_description=$2

    if ! command -v $package_name &> /dev/null; then
        echo "$package_description가 설치되어 있지 않습니다. 설치를 진행합니다."

        # 설치 명령어 (apt-get 사용)
        sudo apt-get install $package_name -y

        # 설치 확인
        if ! command -v $package_name &> /dev/null; then
            echo "$package_description 설치에 실패했습니다."
            missing_packages+="$package_name "
        else
            echo "$package_description가 성공적으로 설치되었습니다."
        fi
    else
        echo "$package_description가 이미 설치되어 있습니다."
    fi
}

install_and_setting_vim() {
    package_name=$1
    package_setting=$2

    sudo apt-get install $package_name -y

    echo "$package_name이 성공적으로 설치되었습니다."

    # 실행할 스크립트 파일 경로
    RELATIVE_DIR=`dirname "$0"`
    SCRIPT_PATH="$RELATIVE_DIR/vimrc.sh"

    # 스크립트 파일이 존재하는지 확인
    if [ -e "$SCRIPT_PATH" ]; then
      # 스크립트 실행
      echo $SCRIPT_PATH
    else
      echo "스크립트 파일이 존재하지 않습니다."
    fi

    echo "$package_setting 설정이 완료됐습니다."
}

# 패키지 설치 확인 및 추가 호출
check_install_package "ifconfig" "ifconfig"
check_install_package "git" "Git"
check_install_package "curl" "Curl"
check_install_package "ssh" "Openssh"
check_install_package "tree" "File Tree Structure"
check_install_package "vlc" "VLC Media Player"

install_and_setting_vim "vim" "vimrc"

check_install "docker-ce" "docker-ce"
check_install "docker-ce-cli" "docker-ce-cli"
check_install "containerd.io" "containerd.io"
check_install "docker-buildx-plugin" "docker-buildx-plugin"
check_install "docker-compose-plugin" "docker-compose-plugin"

# CUDA 설치 확인
if ! command -v nvcc &> /dev/null; then
    echo "CUDA가 설치되어 있지 않습니다. 설치를 진행합니다."

    # CUDA 다운로드 및 설치 명령어
    cuda_version="<CUDA_VERSION>"  # CUDA 버전 (예: 11.4)
    wget https://developer.download.nvidia.com/compute/cuda/repos/ubuntu2004/x86_64/cuda-${cuda_version}_amd64.deb
    sudo dpkg -i cuda-${cuda_version}_amd64.deb
    sudo apt-get update
    sudo apt-get install cuda -y

    # 설치 확인
    if ! command -v nvcc &> /dev/null; then
        echo "CUDA 설치에 실패했습니다."
        missing_packages+="CUDA "
    else
        echo "CUDA가 성공적으로 설치되었습니다."
    fi
else
    echo "CUDA가 이미 설치되어 있습니다."
fi

# cuDNN 설치 확인
if [ ! -f "/usr/include/cudnn.h" ]; then
    echo "cuDNN이 설치되어 있지 않습니다. 설치를 진행합니다."

    # cuDNN 다운로드 명령어
    cudnn_version="<cuDNN_VERSION>"  # cuDNN 버전 (예: 8.2.2)
    wget https://developer.download.nvidia.com/compute/redist/cudnn/v${cudnn_version}/cudnn-${cuda_version}-linux-x64-v${cudnn_version}.tgz
    tar -xzvf cudnn-${cuda_version}-linux-x64-v${cudnn_version}.tgz

    # cuDNN 파일 복사
    sudo cp cuda/include/cudnn.h /usr/include/
    sudo cp cuda/lib64/libcudnn* /usr/lib64/

    # 설치 확인
    if [ ! -f "/usr/include/cudnn.h" ]; then
        echo "cuDNN 설치에 실패했습니다"
        missing_packages+="CUDA "
    else
        echo "CUDNN이 성공적으로 설치되었습니다."
    fi
else
    echo "cuDNN이 이미 설치되어 있습니다."
fi

check_install_nvidia_docker "nvidia-docker2" "nvidia-docker"

# 설치 실패한 패키지 목록 출력
if [ -n "$missing_packages" ]; then
    echo "다음 항목들은 수동으로 설치해야 합니다: $missing_packages"
fi

