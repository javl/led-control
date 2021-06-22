## Software:

1. Download [Raspbian OS Lite](https://www.raspberrypi.org/software/operating-systems/#raspberry-pi-os-32-bit) and flash to SD card (for example using [Balena Etcher](https://www.balena.io/etcher/)).
2. After flashing two partitions appear. In the BOOT partion create a file called `ssh` and a file called `wpa_supplicant.conf`.
Open `wpa_supplicant.conf` and enter the following (replace PASSWORD with the actual password for the network):

```
    ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
    update_config=1
    country=nl

    network={
        ssid="RAEV"
        psk="PASSWORD"
        priority=2
    }

    # Note: you can add multiple network blocks in
    # the same file. The Pi will try to connect to
    # the available network with the highest priority.
    # This is useful when you want to connect to your
    # regular network in the studio and to a different
    # network during a performance.
```
3. Plug in the SD card and power the RPi. After a few seconds it should connect to the network. Check your router to find the Pi's IP address.
4. SSH into the pi: `ssh pi@192.168.1.100` (or whatever IP you found). The default RPi password is `raspberry`.
5. Now change this default password! Enter `passwd` and follow the instructions
6. Set a static IP for the pi: `sudo nano /etc/dhcpcd.conf` and add this to the bottom of the file:
```
    interface wlan0
    static ip_address=192.168.1.100
    static routers=192.168.1.1
    static domain_name_servers=192.168.1.1 1.0.0.1
```
7. Reboot the pi (`sudo reboot`). After the reboot the Pi should use our new, static ip `192.168.1.100` (if the router allowed it)
8. SSH back into the RPi using the new IP: `ssh pi@192.168.1.100`
9. Make sure all software is up to date: `sudo apt update && sudo apt upgrade -y`
9. Install some dependencies: `sudo apt install git-core scons swig python3 -y`
10. Clone our code repository: `git clone https://github.com/javl/led-control.git`
11. Enter the new directory and switch to the right branch: `cd led-control; git fetch --all; git checkout artur`
12. Enter the new directory and install the project (nothing might seem to happen for a few minutes): `cd led-control; sudo python3 setup.py develop`
13. Move the startup script to the right location: `sudo mv ledcontrol.service /etc/systemd/system/ledcontrol.service`
14. Enable the service so it starts after boot: `sudo systemctl enable ledcontrol.service`
15. Make sure we can shutdown the Pi as non-root user from the web interface. Open the sudo settings with `sudo visudo` and add the following lines:
```
    pi ALL=(ALL) NOPASSWD: /sbin/reboot, /sbin/shutdown
    root ALL=(ALL) NOPASSWD: /sbin/reboot, /sbin/shutdown
```
16. Just reboot once more to finish `sudo reboot`

## Hardware:
With the ethernet port facing downwards:

```
    ..
    ..
    .x  <-- ground
    ..
    ..
    .x  <-- LED data
    ..
    ..
    ..
    ..
    ..
    ..
    ..
    ..
    ..
    ..
    ..
    ..
    ..
    ..
    ..
```
