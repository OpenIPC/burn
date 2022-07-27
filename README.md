# Burn

## Basic usage

```console
usage: hi35xx-tool [-h] -c
                   {hi3516ev200,hi3520dv100,hi3518ev200,hi3516ev100,hi3518ev201,gk7205v300,hi3516ev300,hi3520dv200,hi3516cv500,hi3556v100,hi3516cv200,hi3516cv300,gk7205v200}
                   -f FILE [-p PORT] [-b] [-d]

options:
  -h, --help            show this help message and exit
  -c {hi3516ev200,hi3520dv100,hi3518ev200,hi3516ev100,hi3518ev201,gk7205v300,hi3516ev300,hi3520dv200,hi3516cv500,hi3556v100,hi3516cv200,hi3516cv300,gk7205v200}, --chip {hi3516ev200,hi3520dv100,hi3518ev200,hi3516ev100,hi3518ev201,gk7205v300,hi3516ev300,hi3520dv200,hi3516cv500,hi3556v100,hi3516cv200,hi3516cv300,gk7205v200}
                        Chip model name
  -f FILE, --file FILE  U-Boot binary file to load
  -p PORT, --port PORT  Serial port device name
  -b, --break           Send Ctrl-C just after load
  -d, --debug           Set debug mode
```

### CV300

```
./hi35xx-tool --chip hi3516cv300 --file=u-boot/hi3516cv300.bin
```

### EV300

Download special [recovery mode
version](https://github.com/OpenIPC/openipc-2.1/releases/download/latest/u-boot-hi3516ev300-beta.bin)
of U-Boot.

```console
$ ./hi35xx-tool --chip hi3516ev200 --file=u-boot-hi3516ev300-beta.bin ; screen -L /dev/ttyUSB0 115200
```

## U-Boot continuous integration

Real world example on U-Boot developing for CV300 board:

```bash
set -e

# In case of buggy USB UART adapter
sudo usbreset /dev/bus/usb/005/007

# In U-Boot directory:
make ARCH=arm CROSS_COMPILE=arm-hisiv500-linux- -j$(nproc)
cp u-boot.bin full-boot.bin
cp reg_info_hi3516cv300.bin ./hi3516cv300.reg
make CPU=hi3516cv300 ARCH=arm CROSS_COMPILE=arm-hisiv500-linux- mini-boot.bin

#./mkboot.sh reg_info_hi3516cv300.bin u-boot-ok.bin
cp mini-boot.bin ~/git/burn

cd ~/git/burn
# Custom script to power reset camera via network switch
./restart_eth4.sh
./hi35xx-tool --chip hi3516cv300 --file=mini-boot.bin
screen /dev/ttyUSB0 115200
```
