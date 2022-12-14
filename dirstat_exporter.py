import sys
import time
from pathlib import Path
from prometheus_client import start_http_server, Gauge, Info


SCAN_DIR = Path(sys.argv[1])
SLEEP_INTERVAL_SEC = int(sys.argv[2])
PORT = int(sys.argv[3])

metrics = {}
start_http_server(PORT)


while True:

    files_count = 0
    files_size_bytes = 0
    for item in SCAN_DIR.glob('*'):
        if item.exists() and item.is_file():
            file_stat = item.stat()
            files_count += 1
            files_size_bytes += file_stat.st_size
    
    metric_name = f"files_count"
    if metric_name not in metrics.keys():
        metrics[metric_name] = Gauge(metric_name, '', ['dir'])
    metrics[metric_name].labels(dir=SCAN_DIR.as_posix()).set(files_count)

    metric_name = f"files_size_bytes"
    if metric_name not in metrics.keys():
        metrics[metric_name] = Gauge(metric_name, '', ['dir'])
    metrics[metric_name].labels(dir=SCAN_DIR.as_posix()).set(files_size_bytes)
                
    time.sleep(SLEEP_INTERVAL_SEC)
