# Burn

### Video Tutorials

[OpenIPC BURN Utility Playlist][youtube_burn]

## Basic usage

```console
usage: burn [-h] -c
                   {hi3516ev200,hi3520dv100,hi3518ev200,hi3516ev100,hi3518ev201,gk7205v300,hi3516ev300,hi3520dv200,hi3516cv500,hi3556v100,hi3516cv200,hi3516cv300,gk7205v200}
                   -f FILE [-p PORT] [-b] [-d]

options:
  -h, --help            show this help message and exit
  -c {hi3516ev200,hi3520dv100,hi3518ev200,hi3516ev100,hi3518ev201,gk7205v300,hi3516ev300,hi3520dv200,hi3516cv500,hi3556v100,hi3516cv200,hi3516cv300,gk7205v200}, --chip {hi3516ev200,hi3520dv100,hi3518ev200,hi3516ev100,hi3518ev201,gk7205v300,hi3516ev300,hi3520dv200,hi3516cv500,hi3556v100,hi3516cv200,hi3516cv300,gk7205v200}
                        Chip model name
  -f FILE, --file FILE  U-Boot binary file to upload
  -p PORT, --port PORT  Serial port device name
  -b, --break           Send Ctrl-C just after upload
  -d, --debug           Set debug mode
```

If burn complains about **missing python modules**, you should install the list of modules by running:

```
pip install -r requirements.txt
```

### CV300

```
./burn --chip hi3516cv300 --file=u-boot/hi3516cv300.bin
```

### EV300

Download special [recovery mode
version](https://github.com/OpenIPC/firmware/releases/download/latest/u-boot-hi3516ev300-universal.bin)
of U-Boot.

```console
$ ./burn --chip hi3516ev200 --file=u-boot-hi3516ev300-beta.bin --break; screen -L /dev/ttyUSB0 115200
```

### Unlock flash on gk7205v200

```console
$ ./burn --chip gk7205v200 --file=u-boot/gk7205v200.bin --break; screen -L /dev/ttyUSB0 115200
goke # sf probe
@do_spi_flash_probe() flash->erase_size: 65536, flash->sector_size: 0
goke # sf lock 0
unlock all block.
```

### Unlock flash on gk7205v300

```console
$ ./burn --chip gk7205v300 --file=u-boot/gk7205v300.bin --break; screen -L /dev/ttyUSB0 115200
goke # sf probe
@do_spi_flash_probe() flash->erase_size: 65536, flash->sector_size: 0
goke # sf lock 0
unlock all block.
```

### Start kernel from memory

```console
setenv ipaddr 192.168.1.1; setenv serverip 192.168.1.10; mw.b 0x42000000 ff 1000000; tftpboot 0x42000000 uImage.${soc}; bootm 0x42000000
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
./burn --chip hi3516cv300 --file=mini-boot.bin
screen /dev/ttyUSB0 115200
```

[youtube_burn]: https://youtube.com/playlist?list=PLh0sgk8j8CfsMPq9OraSt5dobTIe8NXmw
