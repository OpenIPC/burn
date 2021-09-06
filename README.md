# Burn

## Basic usage

```console
$ ./hi35xx-tool --chip <chip> --type=<ddr,spi,nand> --file=<file.bin> --port=<comport> --debug
```

where

* `--chip=<chip>`  -  chipname, for example "hi3520dv200"

* `--type=<ddr,spi,nand>`  -  loading type, ddr or spi or nand

* `--file=<file.bin>`  -  uboot.bin, bootloader for selected chip

* `--port=<comport>`  -  uart port, by default /dev/ttyUSB0

* `--debug or -d`  -  print more info

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
