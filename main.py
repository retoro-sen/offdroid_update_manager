import shutil
import subprocess
import re
from datetime import datetime

def print_banner():
    """Display the offdroid banner"""
    banner = """
╔═══════════════════════════════════════════════╗
║                                               ║
║     ╔═╗╔═╗╔═╗╔╦╗╦═╗╔═╗╦╔╦╗                    ║
║     ║ ║╠╣ ╠╣  ║║╠╦╝║ ║║ ║║                    ║
║     ╚═╝╚  ╚   ╩╝╩╚═╚═╝╩═╩╝                    ║
║                                               ║
║   Cross-Platform Update Manager v1.0          ║
║                                               ║
╚═══════════════════════════════════════════════╝
    """
    print(banner)

print_banner()
print("🤖 Detecting operating system and package manager...")

def parse_update_output(pm, output):
    """Parse package manager output to extract updated packages"""
    updated_packages = []
    
    if pm == "apt":
        # Parse apt output for upgraded packages
        for line in output.split('\n'):
            if line.startswith('Unpacking') or line.startswith('Setting up'):
                match = re.search(r'(Unpacking|Setting up) ([\w\-\.]+)', line)
                if match:
                    pkg = match.group(2)
                    if pkg not in updated_packages:
                        updated_packages.append(pkg)
    
    elif pm == "zypper":
        # Parse zypper output
        in_packages = False
        for line in output.split('\n'):
            if 'The following' in line and 'package' in line:
                in_packages = True
                continue
            if in_packages and line.strip():
                packages = line.strip().split()
                updated_packages.extend(packages)
    
    elif pm == "dnf":
        # Parse dnf output
        for line in output.split('\n'):
            if line.startswith('Upgrading') or line.startswith('Installing'):
                match = re.search(r'(Upgrading|Installing)\s+:\s+([\w\-\.]+)', line)
                if match:
                    updated_packages.append(match.group(2))
    
    elif pm == "pacman":
        # Parse pacman output
        for line in output.split('\n'):
            if 'upgrading' in line.lower():
                match = re.search(r'upgrading ([\w\-\.]+)', line, re.IGNORECASE)
                if match:
                    updated_packages.append(match.group(1))
    
    elif pm == "brew":
        # Parse brew output
        for line in output.split('\n'):
            if line.startswith('==>') and 'Upgrading' in line:
                match = re.search(r'Upgrading ([\w\-\.]+)', line)
                if match:
                    updated_packages.append(match.group(1))
    
    return updated_packages

def updates():
    if shutil.which("apt-get"):
        pm = "apt"
    elif shutil.which("zypper"):
        pm = "zypper"
    elif shutil.which("dnf"):
        pm = "dnf"
    elif shutil.which("pacman"):
        pm = "pacman"
    elif shutil.which("brew"):
        pm = "brew"
    else:
        print("🤖 Checking package manager...")
        print("❌ No supported package manager found (apt, zypper, dnf, pacman, or brew).")
        return False
    #Get confirmation
    ans = input("Do you want to search for and install updates? (yes/no): ").strip().lower()
    if ans != "yes":
        print("Aborted by user.")
        return False
    
    updated_packages = []
    
    try:
       if pm == "apt":
           print("Starting apt update...")
           subprocess.run(["sudo", "apt-get", "update"], check=True)
           print("Installing updates...")
           result = subprocess.run(["sudo", "apt-get", "upgrade", "-y"], 
                                 capture_output=True, text=True, check=True)
           updated_packages = parse_update_output(pm, result.stdout)
           
       elif pm == "zypper":
           print("Oh, an openSUSE user. Starting zypper update...")
           subprocess.run(["sudo", "zypper", "refresh"], check=True)
           print("Installing updates...")
           result = subprocess.run(["sudo", "zypper", "update", "-y"], 
                                 capture_output=True, text=True, check=True)
           updated_packages = parse_update_output(pm, result.stdout)
           
       elif pm == "dnf":
           print("Starting dnf update...")
           subprocess.run(["sudo", "dnf", "check-update"], check=False)
           print("Installing updates...")
           result = subprocess.run(["sudo", "dnf", "upgrade", "-y"], 
                                 capture_output=True, text=True, check=True)
           updated_packages = parse_update_output(pm, result.stdout)
           
       elif pm == "pacman":
           print("Oh, an Arch user. Starting pacman update...")
           subprocess.run(["sudo", "pacman", "-Sy"], check=True)
           print("Installing updates...")
           result = subprocess.run(["sudo", "pacman", "-Su", "--noconfirm"], 
                                 capture_output=True, text=True, check=True)
           updated_packages = parse_update_output(pm, result.stdout)
           
       elif pm == "brew":
           print("Oh, a Mac user. Starting brew update...")
           subprocess.run(["brew", "update"], check=True)
           print("Installing updates...")
           result = subprocess.run(["brew", "upgrade"], 
                                 capture_output=True, text=True, check=True)
           updated_packages = parse_update_output(pm, result.stdout)
           
    except subprocess.CalledProcessError as e:  
        print("❌ There was a problem installing the updates.")
        print(e)
        return False
    
    print("\n✅ Updates were successfully installed!")
    
    # Display changelog
    if updated_packages:
        print(f"\n📦 Updated packages ({len(updated_packages)}):")
        print("=" * 50)
        for pkg in updated_packages:
            print(f"  • {pkg}")
        print("=" * 50)
    else:
        print("\nℹ️  No packages were updated (system might be already up-to-date)")
    
    return True

# Call function
if __name__ == "__main__":
    updates()
