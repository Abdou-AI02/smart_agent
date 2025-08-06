import psutil
import platform
import os

class SystemMonitor:
    def __init__(self):
        self.os_info = platform.system()

    def get_cpu_usage(self):
        """Returns current CPU usage percentage."""
        return psutil.cpu_percent(interval=1)

    def get_ram_usage(self):
        """Returns current RAM usage details."""
        mem = psutil.virtual_memory()
        return {
            "total": f"{mem.total / (1024**3):.2f} GB",
            "available": f"{mem.available / (1024**3):.2f} GB",
            "percent": mem.percent
        }

    def get_disk_usage(self, path='/'):
        """Returns disk usage for a given path (default root)."""
        if self.os_info == "Windows":
            path = os.path.splitdrive(os.getcwd())[0] + '\\'
        elif self.os_info == "Darwin":
             path = '/'
        
        try:
            disk = psutil.disk_usage(path)
            return {
                "total": f"{disk.total / (1024**3):.2f} GB",
                "used": f"{disk.used / (1024**3):.2f} GB",
                "free": f"{disk.free / (1024**3):.2f} GB",
                "percent": disk.percent
            }
        except Exception as e:
            return {"error": f"Could not get disk usage for path '{path}': {e}"}

    def get_system_summary(self):
        """Returns a summary of system resources."""
        cpu = self.get_cpu_usage()
        ram = self.get_ram_usage()
        disk = self.get_disk_usage()
        
        summary = f"System Summary ({self.os_info}):\n"
        summary += f"  CPU Usage: {cpu}%\n"
        summary += f"  RAM: {ram['percent']}% used ({ram['available']} available out of {ram['total']})\n"
        if "error" not in disk:
            summary += f"  Disk Usage: {disk['percent']}% used ({disk['free']} free out of {disk['total']})\n"
        else:
            summary += f"  Disk Usage: {disk['error']}\n"
        return summary