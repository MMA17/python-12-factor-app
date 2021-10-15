from typing import Counter
from urllib import request
from prometheus_client import start_http_server, Summary, Gauge
import time
import psutil

# REQUEST_TIME = Summary('request_processing_seconds', 'Time spent processing request')
# # Decorate function with metric.
# @REQUEST_TIME.time()
# def process_request(t):
#     """A dummy function that takes some time."""
#     time.sleep(t)

cpu_usage = Gauge('cpu_usage', 'Number of precent cpu using', labelnames=['cputype'])
def get_cpu_percent():
    cpu_usage.labels(cputype='intel').set(psutil.cpu_percent())

ram_usage = Gauge('ram_usage', 'Number of precent cpu using', labelnames=['type'])
def get_ram_percent():
    ram_usage.labels(type='precent').set(psutil.virtual_memory().percent)
    ram_usage.labels(type='total').set(psutil.virtual_memory().total)
    ram_usage.labels(type='free').set(psutil.virtual_memory().free)
    ram_usage.labels(type='used').set(psutil.virtual_memory().used)

network = Gauge('network_info', 'Infomation about network bandwidth', labelnames=['type'])
def get_network_info():
    network.labels(type='inbound_bytes_total').set(psutil.net_io_counters().bytes_recv)
    network.labels(type='outbound_bytes_total').set(psutil.net_io_counters().bytes_sent)
    network.labels(type='inbound_packet_total').set(psutil.net_io_counters().packets_recv)
    network.labels(type='outbound_packet_total').set(psutil.net_io_counters().packets_sent)

 
bandwidth = Gauge('network_bandwidth', 'Infomation about network bandwidth', labelnames=['type'])
def convert_to_kbit(value):
    return value/1024.*8

if __name__ == '__main__':

    start_http_server(8000)
    bw_outbound_old_value = 0
    bw_inbound_old_value = 0
    while True:
        get_cpu_percent()
        get_ram_percent()
        get_network_info()

        # Calculate bandwidth real-time
        bw_outboud_new_value = psutil.net_io_counters().bytes_sent 
        if bw_outbound_old_value:
            bandwidth.labels('outbound').set("%0.3f" % convert_to_kbit(bw_outboud_new_value - bw_outbound_old_value))
        bw_outbound_old_value = bw_outboud_new_value

        bw_inboud_new_value = psutil.net_io_counters().bytes_recv 
        if bw_inbound_old_value:
            bandwidth.labels('inbound').set("%0.3f" % convert_to_kbit(bw_inboud_new_value - bw_inbound_old_value))
        bw_inbound_old_value = bw_inboud_new_value

        time.sleep(1)