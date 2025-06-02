# iBootMe
**A Python-based tool with tkinter designed for flashing IPSWs and managing them.** \
This is a frontend for idevicerestore, part of the libimobiledevice library.

## Dependencies
- **Linux**: `libimobiledevice, usbmuxd, Python3`

## Installation
### Linux
1. Clone the repository and navigate to it:

```bash
git clone https://github.com/naturelessGit/iBootMe.git
cd iBootMe
```

2. Install the required dependencies:

```bash
sudo apt install usbmuxd libimobiledevice python3 python3-tk
```

(Package manager may vary depending on your system.)

3. It is highly reccomended to use a virtual enviroment:

```bash
python3 -m venv .env
source .env/bin/activate
```

4. Run the application:

```bash
python3 main.py
```

## Flashing
1. Connect your phone to your computer. You can use your charging cable. 
2. Install and run iBootMe. 
3. Choose your options. If your a casual user, you may not need to tinker with the advanced options 
4. Click the "Flash!" button. If you encounter an issue, you can copy and paste the output and report the issue on our GitHub.

## Will there be a macOS / Windows version eventually?
Probably! A macOS / Windows export and distribution will be released soon.

## Authors 
This project is made with love by Natureless

