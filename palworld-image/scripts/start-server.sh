#!/bin/bash

echo "Starting Server"

COMMAND="/palworld/PalServer.sh"

COMMAND_ARGS=""

COMMAND_ARGS="${COMMAND_ARGS} -port ${PORT}"
COMMAND_ARGS="${COMMAND_ARGS} -players ${PLAYERS}"

if [ "${COMMUNITY}" = "true" ]; then
    COMMAND_ARGS="${COMMAND_ARGS} EpicApp=PalServer"

    echo "Community Server Enabled"
fi

if [ -n "${SERVER_PASSWORD}" ]; then
    COMMAND_ARGS="${COMMAND_ARGS} -serverpassword ${SERVER_PASSWORD}"

    echo "Server Protected With Password"
fi

if [ -n "${SERVER_NAME}" ]; then
    COMMAND_ARGS="${COMMAND_ARGS} -servername ${SERVER_NAME}"

    echo "Server Name Enabled"
else
    echo "Warning: No Server Name Set"
fi

if [ -n "${ADMIN_PASSWORD}" ]; then
    COMMAND_ARGS="${COMMAND_ARGS} -adminpassword=${ADMIN_PASSWORD}"
    echo "Admin Password Set"
else
    echo "Warning: No Admin Password Set"
fi

if [ "${MULTITHREADING}" = "true" ]; then
    COMMAND_ARGS="${COMMAND_ARGS} -useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS"

    echo "Multithreading Enabled"
else
    echo "Warning: Multithreading Disabled"
fi

if [ -n "${PUBLIC_IP}" ]; then
    COMMAND_ARGS="${COMMAND_ARGS} -publicip=${PUBLIC_IP}"

    echo "Public IP Defined"
fi

if [ -n "${PUBLIC_PORT}" ]; then
    COMMAND_ARGS="${COMMAND_ARGS} -publicport=${PORT}"

    echo "Public Port Defined"
fi

echo "Processed Arguments"
echo "${COMMAND_ARGS}"

su steam -c "${COMMAND} ${COMMAND_ARGS}"