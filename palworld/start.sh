COMMAND="/app/PalServer.sh"

COMMAND="${COMMAND} -port ${PALWORLD_PORT}"
COMMAND="${COMMAND} -players ${PALWORLD_PLAYERS}"

if [ "${COMMUNITY}" = "true" ]; then
    COMMAND="${COMMAND} EpicApp=PalServer"

    if [ -n "${SERVER_PASSWORD}" ]; then
        COMMAND="${COMMAND} -serverpassword ${SERVER_PASSWORD}"
    fi

    if [ -n "${SERVER_NAME}" ]; then
        COMMAND="${COMMAND} -servername ${SERVER_NAME}"
    fi
fi

if [ "${MULTITHREADING}" = "true" ]; then
    COMMAND="${COMMAND} -useperfthreads -NoAsyncLoadingThread -UseMultithreadForDS"
fi

if [ -n "${PUBLIC_IP}" ]; then
    COMMAND="${COMMAND} -publicip=${PUBLIC_IP}"
fi

if [ -n "${PUBLIC_PORT}" ]; then
    COMMAND="${COMMAND} -publiport=${PUBLIC_PORT}"
fi

su steam -c "${COMMAND}"