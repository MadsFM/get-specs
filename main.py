import platform
import socket
import psutil
import cpuinfo
import GPUtil


class Hardware:
    def __init__(self, name):
        self.name = name

    def get_info(self):
        self = self

class CPU(Hardware):
    def __init__(self):
        super().__init__("CPU")
        self.brand = cpuinfo.get_cpu_info()["brand_raw"]
        self.cores = psutil.cpu_count(logical=False)
        self.usage = psutil.cpu_percent(interval=1)

    def get_info(self):
        return f"{self.name}: {self.brand}, Cores: {self.cores}, Usage: {self.usage}%"

class GPU(Hardware):
    def __init__(self):
        super().__init__("GPU")
        self.gpus = GPUtil.getGPUs()

    def get_info(self):
        if not self.gpus:
            return "No GPU, superior race!"
        return "\n".join([f"{gpu.name} ({gpu.memoryTotal} MB" for gpu in self.gpus])

class RAM(Hardware):
    def __init__(self):
        super().__init__("RAM")
        self.total_memory = round(psutil.virtual_memory().total / (1024 ** 3), 2)
        self.used_memory = round(psutil.virtual_memory().used / (1024 ** 3), 2)

    def get_info(self):
        return f"{self.name}: {self.used_memory} GB / {self.total_memory} GB"

class HDD(Hardware):
    def __init__(self):
        super().__init__("HDD")
        self.partitions = psutil.disk_partitions()
        self.total_storage = sum(psutil.disk_usage(part.mountpoint).total for part in self.partitions if part.fstype)
        self.used_storage = sum(psutil.disk_usage(part.mountpoint).used for part in self.partitions if part.fstype)
        self.total_storage_gb = round(self.total_storage / (1024 ** 3), 2)
        self.used_storage_gb = round(self.used_storage / (1024 ** 3), 2)

    def get_info(self):
        return f"{self.name}: {self.used_storage_gb} GB / {self.total_storage_gb} GB"

class SystemInfo:
    def __init__(self):
        self.hostname = socket.gethostname()
        self.system = platform.system()
        self.architecture = platform.architecture()
        self.kernel = platform.release()
        self.compiler = platform.python_compiler()

    def get_info(self):
        return (f"\n"
                f"Hostname: {self.hostname}\n"
                f"System: {self.system}\n"
                f"Architecture: {self.architecture}\n"
                f"Kernel: {self.kernel}\n"
                f"Python Compiler: {self.compiler}"
                f" \n")

if __name__ == "__main__":
    cpu = CPU()
    gpu = GPU()
    ram = RAM()
    hdd = HDD()
    system = SystemInfo()

    print(system.get_info())
    print(gpu.get_info())
    print(cpu.get_info())
    print(ram.get_info())
    print(hdd.get_info())