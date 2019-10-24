#!/bin/sh
# Switch to normal user on alpine-based docker containers.
# Dependencies: su-exec

username=$EXEC_USER
userid=${EXEC_USER_ID}
permission=${EXEC_PERMISSION}

echo "Summoning $username - UID:$userid ..."

# Add local user
adduser $username -u $userid -D -s /bin/sh
chown -R $username .
chmod -R $permission .
exec su-exec $username "$@"