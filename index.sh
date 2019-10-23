#!/bin/sh
# Switch to normal user on alpine-based docker containers.
# Dependencies: su-exec

username=$EXEC_USER
userid=${EXEC_USER_ID}

folder=$1
permission=$2

: ${folder:="."}
: ${permission:=755}

echo "Summoning $username - UID:$userid ..."

# Add local user
adduser $username -u $userid -D -s /bin/sh
chown -R $username $folder
chmod -R $permission $folder
exec su-exec $username "$@"