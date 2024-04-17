#!/bin/sh


### BEGIN INIT INFO
# Provides:          v2xadmin
# Required-Start:    v2xservices
# Required-Stop:
# Default-Start:     2 3 4 5
# Default-Stop:
# Short-Description: Handle V2X Virtual admin services
# Description:       Handle V2X Virtual admin services
### END INIT INFO

start() {
    echo -n "Starting v2xadmin service:"
    export LD_LIBRARY_PATH=/mnt/spirent/bll/Python/lib:$LD_LIBRARY_PATH
    export V2X_ADMIN=/mnt/spirent/v2x-admin
    export V2X_ADMIN_PYTHON=${V2X_ADMIN}/venv/bin/python
    export FLASK_APP=${V2X_ADMIN}/app.py
    export V2X_CERT=${V2X_ADMIN}/cert

    rm ${V2X_ADMIN_PYTHON}

    ln -s /mnt/spirent/bll/Python/bin/python ${V2X_ADMIN_PYTHON}

    ${V2X_ADMIN_PYTHON} -m flask run --cert=${V2X_CERT}/cv2x.crt --key=${V2X_CERT}/cv2x.key --host="0.0.0.0" --port=58887 >/dev/null 2>&1 &

    echo "OK"
}

stop() {
    # Get the PID of the process
    pid=$(pgrep -f '/mnt/spirent/v2x-admin/venv/bin/python -m flask run --cert=/mnt/spirent/v2x-admin/cert/cv2x.crt --key=/mnt/spirent/v2x-admin/cert/cv2x.key --host=0.0.0.0 --port=58887')

    # Stop the process
    if [ -n "$pid" ]; then
        echo -n "Stopping v2xadmin service: "
        kill $pid
        echo "OK."
    else
        echo "Service is not running."
    fi
}

restart() {
    stop
    sleep 2
    start
}

case "$1" in
    start)
        start
        ;;
    stop)
        stop
        ;;
    restart)
        restart
        ;;
    *)
        echo "Usage: $0 {start|stop|restart}"
        exit 1
esac

exit 0