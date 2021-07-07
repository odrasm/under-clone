#export DEBUG="--debug"
export DEBUG=""
#export TESTING="true"
export TESTING="false"

#export USEDIB="true"
export USEDIB="false"

export BIFROST_TAG="1.0"
export BIFROST_RELEASE="1.0"
export BIFROST_VERSION="11.0.0"
export ANSIBLE_VERSION="'!=2.8.9,<2.9"

#export CAPABILITIES="--net=host --privileged"
#export CAPABILITIES="--privileged"
#export SHARED_DIR="`pwd`/shared"

export NETWORK_INTERFACE="virbr0"
export DHCP_POOL="192.168.122.20-192.168.122.40"

export REGISTRY="nexus01.cloud.e4lab:8082/underground/"
export image_name="underground-bifrost"
export user_name="e4user"

#export CLI="true"
export CLI="false"
