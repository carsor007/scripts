import subprocess
import logging
import sys

svc = str(sys.argv[1])

logging.basicConfig(filename='svc_scp.log',
                    format = '%(asctime)s - %(levelname)s: %(message)s',
                    level=logging.DEBUG)

logging.info('Checking if process' + svc + ' is running')

service_is_running = subprocess.call(["ps", "-C", svc])

if service_is_running == 1:
    logging.warning('Process' + svc + ' is not running')
    logging.info('Attempting to restart: ' + svc)
    restart_sts = subprocess.call(["sudo", "/etc/init.d/%s" % svc, "start"])
    if restart_sts == 1:
        logging.error("Unable to restart %s please check the logs" % svc)
    else:
        logging.info("%s successfully restarted" % svc)
else:
    logging.info("%s is currently running" % svc)

