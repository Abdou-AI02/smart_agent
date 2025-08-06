import os
import hashlib
import platform
import subprocess
from config import SUSPICIOUS_PATHS
from utils.helper_functions import hash_file

class SecurityHandler:
    def __init__(self):
        self.base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        self.integrity_file = os.path.join(self.base_dir, 'data', 'integrity_checksums.json')
        self.platform = platform.system()

    def _get_project_files(self):
        """Gets all Python files in the project to check their integrity."""
        file_list = []
        for root, _, files in os.walk(self.base_dir):
            for file in files:
                if file.endswith('.py') or file.endswith('.md'):
                    file_list.append(os.path.join(root, file))
        return file_list

    def create_integrity_baseline(self):
        """
        Generates a baseline of file hashes for integrity checking.
        This should be run once after a clean installation.
        """
        checksums = {}
        file_list = self._get_project_files()
        for file in file_list:
            checksums[file] = hash_file(file)
        
        try:
            with open(self.integrity_file, 'w') as f:
                import json
                json.dump(checksums, f, indent=4)
            return "Integrity baseline created successfully."
        except Exception as e:
            return f"Error creating integrity baseline: {e}"

    def run_integrity_check(self):
        """Checks the current project files against the saved integrity baseline."""
        if not os.path.exists(self.integrity_file):
            return "Integrity baseline not found. Please run 'create integrity baseline' first."
        
        try:
            with open(self.integrity_file, 'r') as f:
                import json
                baseline_checksums = json.load(f)
        except Exception as e:
            return f"Error loading integrity baseline: {e}"

        current_files = self._get_project_files()
        results = []
        
        for file in current_files:
            current_hash = hash_file(file)
            baseline_hash = baseline_checksums.get(file)
            
            if not baseline_hash:
                results.append(f"⚠️ NEW FILE DETECTED: {file}")
            elif current_hash != baseline_hash:
                results.append(f"🚨 INTEGRITY WARNING: File changed: {file}")

        if not results:
            return "Project files integrity check passed. No changes detected."
        else:
            return "Project files integrity check completed with warnings:\n" + "\n".join(results)

    def get_security_status(self):
        """Provides a basic security summary of the system."""
        summary = f"Security Status for {self.platform}:\n"
        
        # Check Firewall Status (OS-specific)
        if self.platform == 'Windows':
            try:
                # Use 'netsh' command to check firewall state
                output = subprocess.check_output(['netsh', 'advfirewall', 'show', 'allprofiles', 'state']).decode('utf-8')
                if "State                  ON" in output:
                    summary += "  Firewall: Enabled ✅\n"
                else:
                    summary += "  Firewall: Disabled ❌ (Recommended to enable)\n"
            except Exception:
                summary += "  Firewall: Status unknown (Error running command) ❓\n"
        elif self.platform == 'Darwin': # macOS
            try:
                # Use 'pfctl' or 'socketfilterfw' on macOS
                output = subprocess.check_output(['/usr/libexec/ApplicationFirewall/socketfilterfw', '--getglobalstate']).decode('utf-8')
                if "Firewall is enabled" in output:
                    summary += "  Firewall: Enabled ✅\n"
                else:
                    summary += "  Firewall: Disabled ❌ (Recommended to enable)\n"
            except Exception:
                summary += "  Firewall: Status unknown (Error running command) ❓\n"
        else:
            summary += "  Firewall: Status check not supported for this OS. ❓\n"

        # Note: This is a very basic check. Full antivirus functionality requires external tools.
        summary += "  Antivirus: No active scan detected. This tool does not provide antivirus functionality.\n"
        
        return summary

    def scan_for_suspicious_files(self):
        """Scans common directories for new, suspicious executable files."""
        suspicious_files = []
        for path in SUSPICIOUS_PATHS:
            if not os.path.exists(path):
                continue
            
            for root, _, files in os.walk(path):
                for file in files:
                    file_path = os.path.join(root, file)
                    # Simple check for executable extensions
                    if file.endswith(('.exe', '.bat', '.cmd', '.vbs', '.sh')):
                        suspicious_files.append(file_path)

        if not suspicious_files:
            return "No suspicious files found in common directories. ✅"
        else:
            message = "⚠️ Suspicious files detected. Please review them manually:\n"
            for f in suspicious_files:
                message += f"- {f}\n"
            return message

    def run_full_security_check(self):
        """Runs a combined security check."""
        status = self.get_security_status()
        integrity = self.run_integrity_check()
        suspicious = self.scan_for_suspicious_files()
        return f"{status}\n\n{integrity}\n\n{suspicious}"