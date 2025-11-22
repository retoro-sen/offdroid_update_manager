#!/usr/bin/env python3
"""
OFFDROID Setup Script
Creates desktop shortcuts with custom pixel robot icon
Installs Python dependencies automatically
Cross-platform support for Linux, macOS, and Windows
"""

import os
import sys
import subprocess
import platform
import shutil
from pathlib import Path

# Pixel Robot Icon in ASCII format for terminal display
ROBOT_ASCII = """
    ████████
  ██▓▓▓▓▓▓██
  ██▓▓▓▓▓▓██
  ██░░██░░██
  ██████████
  ██▓▓▓▓▓▓██
    ██  ██
    ██  ██
  ████  ████
"""

def print_banner():
    """Display setup banner"""
    print("\n" + "="*60)
    print("  OFFDROID SETUP - Automatic Installation")
    print("="*60)
    print(ROBOT_ASCII)
    print("  Installing OFFDROID with pixel robot icon...")
    print("="*60 + "\n")

def check_python():
    """Check if Python version is compatible"""
    print("🔍 Checking Python version...")
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 6):
        print(f"❌ Python 3.6+ required, but found {version.major}.{version.minor}")
        sys.exit(1)
    print(f"✅ Python {version.major}.{version.minor}.{version.micro} detected")
    return True

def install_requirements():
    """Install required packages from requirements.txt"""
    print("\n📦 Installing Python dependencies...")
    req_file = Path(__file__).parent / "requirements.txt"
    
    if not req_file.exists():
        print("ℹ️  No requirements.txt found, skipping dependencies")
        return True
    
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(req_file)],
                      check=True, capture_output=True)
        print("✅ Dependencies installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"⚠️  Warning: Could not install some dependencies: {e}")
        return False

def create_icon_image():
    """Create a pixel robot icon image file"""
    print("\n🎨 Creating pixel robot icon...")
    
    try:
        # Try to use PIL/Pillow if available
        from PIL import Image, ImageDraw
        
        # Create 64x64 pixel icon with transparent background
        size = 64
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Simple color palette
        robot_blue = (66, 133, 244)      # Google Blue
        robot_dark = (51, 103, 214)      # Darker blue
        white = (255, 255, 255)
        antenna_yellow = (251, 188, 5)   # Yellow
        
        # Draw simple robot - centered and symmetrical
        
        # Antenna (top center)
        draw.rectangle([28, 8, 36, 14], fill=antenna_yellow)
        draw.ellipse([26, 4, 38, 10], fill=antenna_yellow)
        
        # Head (rounded rectangle)
        draw.rectangle([20, 16, 44, 32], fill=robot_blue)
        draw.rectangle([20, 16, 44, 18], fill=robot_dark)  # Top edge
        
        # Eyes (simple squares)
        draw.rectangle([24, 20, 28, 24], fill=white)
        draw.rectangle([36, 20, 40, 24], fill=white)
        
        # Eye pupils (small dots)
        draw.rectangle([25, 21, 27, 23], fill=robot_dark)
        draw.rectangle([37, 21, 39, 23], fill=robot_dark)
        
        # Smile
        draw.rectangle([26, 28, 38, 30], fill=white)
        
        # Body (larger rectangle)
        draw.rectangle([18, 34, 46, 52], fill=robot_blue)
        draw.rectangle([18, 34, 46, 36], fill=robot_dark)  # Top edge
        
        # Chest indicator (simple rectangle)
        draw.rectangle([28, 40, 36, 46], fill=robot_dark)
        
        # Arms (simple rectangles)
        draw.rectangle([12, 36, 16, 48], fill=robot_blue)  # Left arm
        draw.rectangle([48, 36, 52, 48], fill=robot_blue)  # Right arm
        
        # Legs (simple rectangles)
        draw.rectangle([22, 52, 30, 60], fill=robot_blue)  # Left leg
        draw.rectangle([34, 52, 42, 60], fill=robot_blue)  # Right leg
        
        # Feet (small rectangles at bottom)
        draw.rectangle([20, 60, 30, 62], fill=robot_dark)  # Left foot
        draw.rectangle([34, 60, 44, 62], fill=robot_dark)  # Right foot
        
        icon_path = Path(__file__).parent / "offdroid_icon.png"
        img.save(icon_path)
        print(f"✅ Icon created: {icon_path}")
        return str(icon_path)
        
    except ImportError:
        print("ℹ️  Pillow not available, creating simple icon...")
        # Fallback: Create a simple icon file marker
        icon_path = Path(__file__).parent / "offdroid_icon.txt"
        with open(icon_path, 'w') as f:
            f.write(ROBOT_ASCII)
        print(f"✅ Icon marker created: {icon_path}")
        return str(icon_path)
    except Exception as e:
        print(f"⚠️  Could not create icon: {e}")
        return None

def create_desktop_shortcut(icon_path=None):
    """Create desktop shortcut based on OS"""
    print("\n🔗 Creating desktop shortcut...")
    
    system = platform.system()
    script_path = Path(__file__).parent / "main.py"
    
    try:
        if system == "Linux":
            # Create .desktop file for Linux
            desktop_file = Path.home() / ".local" / "share" / "applications" / "offdroid.desktop"
            desktop_file.parent.mkdir(parents=True, exist_ok=True)
            
            with open(desktop_file, 'w') as f:
                f.write("[Desktop Entry]\n")
                f.write("Version=1.0\n")
                f.write("Type=Application\n")
                f.write("Name=OFFDROID\n")
                f.write("Comment=Cross-Platform Update Manager\n")
                f.write(f"Exec=python3 {script_path}\n")
                f.write(f"Path={script_path.parent}\n")
                if icon_path:
                    f.write(f"Icon={icon_path}\n")
                f.write("Terminal=true\n")
                f.write("Categories=System;Utility;\n")
            
            os.chmod(desktop_file, 0o755)
            print(f"✅ Desktop entry created: {desktop_file}")
            
        elif system == "Darwin":  # macOS
            # Create app bundle or alias
            app_name = "OFFDROID.app"
            app_path = Path.home() / "Applications" / app_name
            
            # Create simple shell script launcher
            launcher = Path(__file__).parent / "offdroid_launcher.command"
            with open(launcher, 'w') as f:
                f.write("#!/bin/bash\n")
                f.write(f"cd {script_path.parent}\n")
                f.write(f"python3 {script_path}\n")
            
            os.chmod(launcher, 0o755)
            print(f"✅ Launcher created: {launcher}")
            print("   You can drag this to your Dock for quick access")
            
        elif system == "Windows":
            # Create Windows shortcut
            try:
                import winshell
                from win32com.client import Dispatch
                
                desktop = winshell.desktop()
                shortcut_path = os.path.join(desktop, "OFFDROID.lnk")
                
                shell = Dispatch('WScript.Shell')
                shortcut = shell.CreateShortCut(shortcut_path)
                shortcut.TargetPath = sys.executable
                shortcut.Arguments = f'"{script_path}"'
                shortcut.WorkingDirectory = str(script_path.parent)
                if icon_path:
                    shortcut.IconLocation = icon_path
                shortcut.Description = "OFFDROID - Cross-Platform Update Manager"
                shortcut.save()
                
                print(f"✅ Desktop shortcut created: {shortcut_path}")
            except ImportError:
                # Fallback: Create batch file
                batch_file = Path.home() / "Desktop" / "OFFDROID.bat"
                with open(batch_file, 'w') as f:
                    f.write("@echo off\n")
                    f.write(f'cd /d "{script_path.parent}"\n')
                    f.write(f'python "{script_path}"\n')
                    f.write("pause\n")
                
                print(f"✅ Batch file created: {batch_file}")
        
        return True
        
    except Exception as e:
        print(f"⚠️  Could not create desktop shortcut: {e}")
        return False

def install_pillow():
    """Try to install Pillow for icon creation"""
    print("\n🖼️  Installing Pillow for icon creation...")
    try:
        subprocess.run([sys.executable, "-m", "pip", "install", "Pillow"],
                      check=True, capture_output=True)
        print("✅ Pillow installed successfully")
        return True
    except subprocess.CalledProcessError:
        print("ℹ️  Could not install Pillow, will use fallback icon")
        return False

def make_executable():
    """Make main.py executable on Unix systems"""
    if platform.system() != "Windows":
        script_path = Path(__file__).parent / "main.py"
        try:
            os.chmod(script_path, 0o755)
            print(f"✅ Made {script_path.name} executable")
        except Exception as e:
            print(f"⚠️  Could not make script executable: {e}")

def print_success():
    """Print success message with instructions"""
    system = platform.system()
    script_path = Path(__file__).parent / "main.py"
    
    print("\n" + "="*60)
    print("  🎉 INSTALLATION COMPLETE!")
    print("="*60)
    print("\n📋 How to run OFFDROID:\n")
    
    if system == "Linux":
        print(f"  1. From terminal: python3 {script_path}")
        print(f"  2. From terminal: ./{script_path.name} (if executable)")
        print("  3. From applications menu: Search for 'OFFDROID'")
    elif system == "Darwin":
        print(f"  1. From terminal: python3 {script_path}")
        print("  2. Double-click: offdroid_launcher.command")
        print("  3. Add launcher to Dock for quick access")
    elif system == "Windows":
        print(f"  1. From terminal: python {script_path}")
        print("  2. Double-click desktop shortcut")
        print("  3. Double-click OFFDROID.bat")
    
    print("\n" + "="*60)
    print("  Thank you for using OFFDROID! 🤖")
    print("="*60 + "\n")

def main():
    """Main setup function"""
    print_banner()
    
    # Check Python version
    check_python()
    
    # Install requirements
    install_requirements()
    
    # Try to install Pillow for icon creation
    install_pillow()
    
    # Create icon
    icon_path = create_icon_image()
    
    # Create desktop shortcut
    create_desktop_shortcut(icon_path)
    
    # Make script executable on Unix
    make_executable()
    
    # Print success message
    print_success()

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠️  Setup cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Setup failed: {e}")
        sys.exit(1)
