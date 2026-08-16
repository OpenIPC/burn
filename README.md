# Burn

> [!IMPORTANT]
> ## Burn is superseded by [defib](https://github.com/OpenIPC/defib)
>
> This tool is no longer developed. Use **[defib](https://github.com/OpenIPC/defib)**
> instead — it does everything Burn does and fixes the problems people most often
> hit here.
>
> **Nothing to install — [openipc.github.io/defib](https://openipc.github.io/defib/)**
> runs in Chrome, Edge or Opera. Pick your chip, download the U-Boot image, choose
> your serial port, go. There's a **Dump Flash** button for taking a backup first.
> (Some SoCs still need the CLI — the page tells you which.)
>
> Or install it:
>
> ```sh
> uv tool install defib     # or: pipx install defib
> defib burn -c hi3516ev300 -p /dev/ttyUSB0 -t
> ```
>
> What you get over Burn:
>
> | | Burn | defib |
> |---|---|---|
> | Supported SoCs | 13 | 112 |
> | Protocols | Standard | Standard, V500, CV6xx |
> | macOS | [broken](https://github.com/OpenIPC/burn/issues/16) | fixed (ACK correction) |
> | Flash write when vendor locked the chip | fails silently | handled ([why](https://github.com/OpenIPC/u-boot-gk7205v200/issues/18)) |
> | Full firmware install | manual TFTP | `defib install`, one command |
> | Flash backup / restore | — | yes, with CRC32 verification |
> | Browser UI | — | yes |
>
> **If flashing "succeeded" but the old bootloader is still there**, that is not a
> Burn bug and no amount of `sf lock 0` will fix it — the vendor bootloader set
> `SR3.WPS=1` on the flash and the write was silently discarded. See
> [#8](https://github.com/OpenIPC/burn/issues/8) and
> [#20](https://github.com/OpenIPC/burn/issues/20). `defib agent flash` clears
> those lock bits properly.
>
> The remaining open issues here are kept for their diagnostic value. Please file
> anything new against [OpenIPC/defib](https://github.com/OpenIPC/defib/issues).

## Video Tutorials
![YoutubeScreenshot](https://github.com/OpenIPC/burn/assets/37488/7c19fd75-1806-40c3-901e-ff087f5e35e4)

[OpenIPC BURN Utility Playlist][youtube_burn]

## Archive of current bootloaders for devices

**Please use only this [Archive of current bootloaders for devices][uboot_archive] !!!**

## Features of use in MacOS

**Attention !** Burn does not work reliably on macOS — the USB-serial drivers
corrupt the acknowledgment byte (`0x55` instead of `0xAA`), see
[#16](https://github.com/OpenIPC/burn/issues/16). This is fixed in
[defib](https://github.com/OpenIPC/defib), which corrects the byte automatically;
there is no fix planned for Burn.

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

### HI3516CV300

Download [general
version](https://github.com/OpenIPC/firmware/releases/download/latest/u-boot-hi3516cv300-universal.bin)
of U-Boot.

```
./burn --chip hi3516cv300 --file=u-boot-hi3516cv300-universal.bin --break; screen -L /dev/ttyUSB0 115200
```

### Hi3516EV300

Download [general
version](https://github.com/OpenIPC/firmware/releases/download/latest/u-boot-hi3516ev300-universal.bin)
of U-Boot.

```console
$ ./burn --chip hi3516ev300 --file=u-boot-hi3516ev300-universal.bin --break; screen -L /dev/ttyUSB0 115200
```

### Unlock flash on gk7205v200 and gk7205v210

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
[uboot_archive]: https://github.com/OpenIPC/firmware/releases/tag/latest
