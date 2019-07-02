Suzaku Driver
====================

Suzaku Driver 将 `ipmi-tools` 工具包装为程序工作集， 从 `RabbitMQ` 消费对应指令，提供物理服务器开机/关机/重启/PXE 启动等等基本指令。

## 环境变量

### 环境变量

* LANG=en_US.UTF-8
* LC_ALL=en_US.UTF-8

### 系统变量(/etc/profile.d/suzaku-driver.sh)

```bash
#!/bin/bash
export suzaku-driver_ENV={ "dev" }
```

## 系统工bash

### ubuntubash

* `build-essential`
* `python-dev`
* `libyaml-dev`
* `ipmitool`

### centos

* `gcc`
* `make`
* `automake`
* `autoconf`
* `libtool`
* `python-devel`
* `libyaml-devel`
* `ipmitool`

## 本地调试

```bash
make install
suzaku-driver -e dev
```

## 执行单元测试

```suzaku-driver
make test
```

## 部署和启动


```bash
make deploy
```

## 作者
- jie li
- bo yang
