# offdroid_update_manager
Offdroid - Cross Platform Update Manager for UNIX Systems
# OFFDROID

```
╔═══════════════════════════════════════════════╗
║                                               ║
║     ╔═╗╔═╗╔═╗╔╦╗╦═╗╔═╗╦╔╦╗                   ║
║     ║ ║╠╣ ╠╣  ║║╠╦╝║ ║║ ║║                    ║
║     ╚═╝╚  ╚   ╩╝╩╚═╚═╝╩═╩╝                    ║
║                                               ║
║   Cross-Platform Update Manager v1.0          ║
║                                               ║
╚═══════════════════════════════════════════════╝
```

A smart, cross-platform system update manager that automatically detects your operating system and package manager, then installs updates with a detailed changelog.

## Features

✨ **Automatic OS Detection** - Detects your package manager automatically  
📦 **Update Changelog** - Shows exactly which packages were updated  
🌍 **Cross-Platform Support** - Works on multiple operating systems  
🔒 **Safe Updates** - Asks for confirmation before installing  
📊 **Update Statistics** - Displays count of updated packages  

## Supported Package Managers

| Package Manager | Operating System | Command |
|----------------|------------------|---------|
| **apt** | Debian, Ubuntu, Linux Mint | `apt-get` |
| **zypper** | openSUSE, SUSE Linux | `zypper` |
| **dnf** | Fedora, RHEL, CentOS | `dnf` |
| **pacman** | Arch Linux, Manjaro | `pacman` |
| **brew** | macOS (Homebrew) | `brew` |

## Installation

### Prerequisites

- Python 3.6 or higher
- One of the supported package managers installed
- Sudo privileges (except for Homebrew on macOS)

### Setup

1. Clone the repository:
```bash
git clone https://github.com/retoro-sen/offdroid_update_manager.git
cd offdroid_update_manager
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Make the script executable (optional):
```bash
chmod +x main.py
```

## Usage

Run the script:
```bash
python main.py
```

Or if made executable:
```bash
./main.py
```

### Example Output

```
╔═══════════════════════════════════════════════╗
║     OFFDROID - Cross-Platform Update Manager  ║
╚═══════════════════════════════════════════════╝

🤖 Detecting operating system and package manager...
✓ Detected: apt (Debian/Ubuntu)

Do you want to search for and install updates? (yes/no): yes

Starting apt update...
Installing updates...

✅ Updates were successfully installed!

📦 Updated packages (8):
==================================================
  • firefox
  • linux-headers
  • python3-pip
  • git
  • curl
  • vim
  • nginx
  • docker-ce
==================================================
```

## How It Works

1. **Detection**: Scans your system for available package managers
2. **Confirmation**: Asks for user permission before updating
3. **Update**: Runs the appropriate update commands for your system
4. **Parsing**: Captures and parses the package manager output
5. **Report**: Displays a clean list of all updated packages

## Requirements

See `requirements.txt` for Python dependencies.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

### Ideas for Future Features

- [ ] Update history logging
- [ ] Disk space check before updates
- [ ] Automatic backups before updates
- [ ] Update scheduling
- [ ] Email notifications
- [ ] GUI version

## License

This project is open source and available under the [MIT License](LICENSE).

## Author

Created with ❤️ by [retoro-sen](https://github.com/retoro-sen)

## Support

If you encounter any issues or have questions, please open an issue on [GitHub](https://github.com/retoro-sen/offdroid_update_manager/issues).

---

**Note**: Always ensure you have proper backups before running system updates. This tool requires administrative privileges to install updates on most systems.
