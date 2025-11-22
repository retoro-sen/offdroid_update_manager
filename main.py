import shutil
import subprocess
import re
import os
import sys
import urllib.request
import json
import tempfile
import zipfile
from datetime import datetime
from pathlib import Path

__version__ = "1.1.0"
GITHUB_REPO = "retoro-sen/offdroid_update_manager"
GITHUB_API_URL = f"https://api.github.com/repos/{GITHUB_REPO}/releases/latest"

def print_banner():
    """Display the offdroid banner"""
    banner = """
╔═══════════════════════════════════════════════╗
║                                               ║
║     ╔═╗╔═╗╔═╗╔╦╗╦═╗╔═╗╦╔╦╗                    ║
║     ║ ║╠╣ ╠╣  ║║╠╦╝║ ║║ ║║                    ║
║     ╚═╝╚  ╚   ╩╝╩╚═╚═╝╩═╩╝                    ║
║                                               ║
║   Cross-Platform Update Manager v1.1.0        ║
║                                               ║
╚═══════════════════════════════════════════════╝
    """
    print(banner)

def check_for_updates():
    """Check GitHub for newer version and offer to update"""
    try:
        print("🔍 Checking for OFFDROID updates...")
        
        # Fetch latest release info from GitHub
        req = urllib.request.Request(GITHUB_API_URL)
        req.add_header('User-Agent', 'OFFDROID-Update-Checker')
        
        with urllib.request.urlopen(req, timeout=5) as response:
            data = json.loads(response.read().decode())
            
        latest_version = data.get('tag_name', '').lstrip('v')
        release_notes = data.get('body', 'No release notes available.')
        download_url = data.get('zipball_url', '')
        
        if not latest_version:
            print("ℹ️  Could not determine latest version")
            return
        
        # Compare versions
        def version_tuple(v):
            return tuple(map(int, (v.split("."))))
        
        current = version_tuple(__version__)
        latest = version_tuple(latest_version)
        
        if latest > current:
            print(f"\n🎉 New version available: v{latest_version} (current: v{__version__})")
            print(f"\n📝 Release Notes:\n{release_notes[:300]}...")
            
            ans = input("\n⬇️  Do you want to download and install the update? (yes/no): ").strip().lower()
            
            if ans == "yes":
                download_and_install_update(download_url, latest_version)
            else:
                print("ℹ️  Update skipped. You can update later by running this script again.")
        else:
            print(f"✅ You're running the latest version (v{__version__})")
            
    except urllib.error.URLError:
        print("⚠️  Could not check for updates (no internet connection)")
    except Exception as e:
        print(f"⚠️  Could not check for updates: {e}")

def download_and_install_update(download_url, version):
    """Download and install the latest version"""
    try:
        print(f"\n📥 Downloading version {version}...")
        
        # Get current script directory
        script_dir = Path(__file__).parent.resolve()
        
        # Download to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.zip') as tmp_file:
            tmp_path = tmp_file.name
            
            req = urllib.request.Request(download_url)
            req.add_header('User-Agent', 'OFFDROID-Updater')
            
            with urllib.request.urlopen(req, timeout=30) as response:
                total_size = int(response.headers.get('content-length', 0))
                block_size = 8192
                downloaded = 0
                
                while True:
                    buffer = response.read(block_size)
                    if not buffer:
                        break
                    tmp_file.write(buffer)
                    downloaded += len(buffer)
                    
                    if total_size > 0:
                        percent = (downloaded / total_size) * 100
                        print(f"\rProgress: {percent:.1f}% ({downloaded}/{total_size} bytes)", end='')
        
        print("\n✅ Download complete!")
        print("📦 Installing update...")
        
        # Extract zip file
        with tempfile.TemporaryDirectory() as tmp_dir:
            with zipfile.ZipFile(tmp_path, 'r') as zip_ref:
                zip_ref.extractall(tmp_dir)
            
            # Find the extracted directory (GitHub creates a subdirectory)
            extracted_dirs = [d for d in Path(tmp_dir).iterdir() if d.is_dir()]
            if not extracted_dirs:
                print("❌ Could not find extracted files")
                return
            
            source_dir = extracted_dirs[0]
            
            # Backup current files
            backup_dir = script_dir / f"backup_v{__version__}"
            backup_dir.mkdir(exist_ok=True)
            
            files_to_update = ['main.py', 'setup.py', 'README.md', 'requirements.txt']
            
            for file in files_to_update:
                src_file = script_dir / file
                if src_file.exists():
                    shutil.copy2(src_file, backup_dir / file)
            
            print(f"💾 Backup created: {backup_dir}")
            
            # Copy new files
            for file in files_to_update:
                src_file = source_dir / file
                dst_file = script_dir / file
                if src_file.exists():
                    shutil.copy2(src_file, dst_file)
                    print(f"✅ Updated: {file}")
            
            # Copy docs directory if it exists
            src_docs = source_dir / 'docs'
            dst_docs = script_dir / 'docs'
            if src_docs.exists():
                if dst_docs.exists():
                    shutil.rmtree(dst_docs)
                shutil.copytree(src_docs, dst_docs)
                print("✅ Updated: docs/")
        
        # Cleanup
        os.unlink(tmp_path)
        
        print(f"\n🎉 Successfully updated to version {version}!")
        print("🔄 Please restart OFFDROID to use the new version.")
        print(f"\n💡 Your old files are backed up in: {backup_dir}")
        
        sys.exit(0)
        
    except Exception as e:
        print(f"\n❌ Update failed: {e}")
        print("💡 You can manually download the update from:")
        print(f"   https://github.com/{GITHUB_REPO}/releases/latest")

print_banner()

# Check for updates before running main functionality
check_for_updates()

print("\n🤖 Detecting operating system and package manager...")

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
        # Parse zypper output for OpenSUSE OS
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
        # Parse pacman output for ARCH OS
        for line in output.split('\n'):
            if 'upgrading' in line.lower():
                match = re.search(r'upgrading ([\w\-\.]+)', line, re.IGNORECASE)
                if match:
                    updated_packages.append(match.group(1))
    
    elif pm == "brew":
        # Parse brew output for MacOS
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
        print(f"  • {', '.join(updated_packages)}")
        print("=" * 50)
        
        # Ask to save changelog
        ans = input("\nDo you want to save the changelog to a file? (yes/no): ").strip().lower()
        if ans == "yes":
            filename = f"offdroid_changelog_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w') as f:
                f.write(f"OFFDROID Update Changelog\n")
                f.write(f"Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"Updated packages ({len(updated_packages)}):\n")
                f.write("=" * 50 + "\n")
                f.write(f"  • {', '.join(updated_packages)}\n")
                f.write("=" * 50 + "\n")
            print(f"✅ Changelog saved to {filename}")
    else:
        print("\nℹ️  No packages were updated (system might be already up-to-date)")
    
    return True


# Call function
if __name__ == "__main__":
    updates()
