import platform
import json
import subprocess
import os

# Operating System information
os_info = {
    "system": platform.system(),
    "release": platform.release(),
    "version": platform.version()
}

# Python information
python_info = {
    "version": platform.python_version(),
    "implementation": platform.python_implementation()
}

# CPU information from Windows
cpu_command = [
    "powershell",
    "-NoProfile",
    "-Command",
    "Get-CimInstance Win32_Processor | "
    "Select-Object -First 1 Name, NumberOfCores, "
    "NumberOfLogicalProcessors, MaxClockSpeed | ConvertTo-Json"
]

cpu_result = subprocess.run(
    cpu_command,
    capture_output=True,
    text=True,
    check=True
)

cpu_info = json.loads(cpu_result.stdout)

# CPU specifications
cpu_info["microarchitecture"] = "Kaby Lake"
cpu_info["base_frequency_ghz"] = 2.50
cpu_info["base_frequency_source"] = "Intel processor specification"

# Cache information from Windows
cache_command = [
    "powershell",
    "-NoProfile",
    "-Command",
    "Get-CimInstance Win32_CacheMemory | "
    "Select-Object Purpose, InstalledSize | ConvertTo-Json"
]

cache_result = subprocess.run(
    cache_command,
    capture_output=True,
    text=True,
    check=True
)

cache_info = json.loads(cache_result.stdout)

if isinstance(cache_info, dict):
    cache_info = [cache_info]

cache_profile = {
    "l1_total_kb": None,
    "l1_data_kb": 64,
    "l1_data_kb_per_core": 32,
    "l1_data_source": "Processor specification, 32 KB per core",
    "l2_kb": None,
    "l3_kb": None,
    "cache_line_size_bytes": 64,
    "cache_line_size_source": "Processor specification"
}

for cache in cache_info:
    purpose = cache.get("Purpose", "")
    size = cache.get("InstalledSize")

    if purpose == "L1 Cache":
        cache_profile["l1_total_kb"] = size
    elif purpose == "L2 Cache":
        cache_profile["l2_kb"] = size
    elif purpose == "L3 Cache":
        cache_profile["l3_kb"] = size

# Prepare complete host profile
host_profile = {
    "operating_system": os_info,
    "python": python_info,
    "cpu": cpu_info,
    "cache": cache_profile
}

# Save host profile
project_dir = os.path.dirname(
    os.path.dirname(os.path.abspath(__file__))
)

results_dir = os.path.join(project_dir, "results")
os.makedirs(results_dir, exist_ok=True)

output_path = os.path.join(results_dir, "host_profile.json")

with open(output_path, "w", encoding="utf-8") as file:
    json.dump(host_profile, file, indent=4)

# Display collected information
print("Operating System:", os_info)
print("Python:", python_info)
print("CPU:", cpu_info)
print("Cache:", cache_profile)
print("Host profile saved to:", output_path)
