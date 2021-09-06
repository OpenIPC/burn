# Burn

## Usage

```console
$ ./hi35xx-tool --chip <chip> --type=<ddr,spi,nand> --file=<file.bin> --port=<comport> --debug
```

**where**  

- `--chip=<chip>`  -  chipname, for example "hi3520dv200"
- `--type=<ddr,spi,nand>`  -  loading type, ddr or spi or nand
- `--file=<file.bin>`  -  uboot.bin, bootloader for selected chip
- `--port=<comport>`  -  uart port, by default /dev/ttyUSB0
- `--debug or -d`  -  print more info

### CV300

```
./hi35xx-tool --chip hi3516cv300 --file=u-boot/hi3516cv300.bin
```

### EV300

Download special [recovery
mode](https://github.com/OpenIPC/openipc-2.1/releases/download/latest/u-boot-hi3516ev300-beta.bin)
U-Boot version.

```console
$ ./hi35xx-tool --chip hi3516ev200 --file=u-boot-hi3516ev300-beta.bin ; screen -L /dev/ttyUSB0 115200
```
