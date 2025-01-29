import os
import platform
import subprocess
import socket
from platform import architecture

import psutil
import cpuinfo
import GPUtil

def get_GPU_info():
    gpus = GPUtil.getGPUs()
    if not gpus:
        return "No GPU"
    return "\n".join([f"GPU: {gpu.name} ({gpu.memoryTotal}) MB" for gpu in gpus])

def get_system_info():
    hostname = socket.gethostname()
    system = platform.system()
    architecture = platform.architecture()
    kernel = platform.release()
    compiler = platform.python_compiler()
    cpu = cpuinfo.get_cpu_info()["brand_raw"]
    cores = psutil.cpu_count(logical=True)
    memory = round(psutil.virtual_memory().total / (1024 ** 3))
    disk = round(psutil.disk_usage('/').total / (1024 ** 3))

    return f"""
-----System info-----

Hostname: {hostname}
System: {system} {architecture}
Kernel: {kernel}
Compiler: {compiler}
CPU: {cpu} ({cores} Core)
Memory: {memory} GB
HDD: {disk} GB

-----GPU-----
{get_GPU_info()}

-----Usage-----

RAM used : {round(psutil.virtual_memory().used / (1024 ** 3))} GB / {memory} GB ( {psutil.virtual_memory().percent} % )
HDD used : {round(psutil.disk_usage('/').used / (1024 ** 3))} GB / {disk} GB ( {psutil.disk_usage('/').percent} % )

"""

print(get_system_info())