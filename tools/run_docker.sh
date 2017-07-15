#!/bin/bash
package_name="$1"
if [ -z "$package_name" ]
then
    &>2 echo "Please pass package name as a first argument of this script ($0)"
    exit 1
fi

manylinux1_image_prefix="quay.io/pypa/manylinux1_"
dock_ext_args=""

for arch in x86_64 i686
do
    docker pull "${manylinux1_image_prefix}${arch}" &
    export docker_pull_pid_${arch}=$!
done

for arch in x86_64 i686
do
    arch_pull_pid=$(eval echo \$docker_pull_pid_${arch})
    echo Waiting for docker pull PID $arch_pull_pid to complete downloading container for $arch arch...
    wait $arch_pull_pid  # await for docker image for current arch to be pulled from hub
    [ $arch == "i686" ] && dock_ext_args="linux32"

    echo Building wheel for $arch arch
    docker run --rm -v `pwd`:/io "${manylinux1_image_prefix}${arch}" $dock_ext_args /io/tools/build-wheels.sh "$package_name"

    dock_ext_args=""  # Reset docker args, just in case
done
