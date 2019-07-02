Suzaku Driver RabbitMQ Command
===========================================

### ping ilo ip

```json
{
    "sn" : "sn-xxx",
    "action" : "PingHost",
    "ip" : "192.168.56.10"
}
```

### pxe boot

```json
{
    "sn" : "sn-xxx",
    "action" : "SetPXEBoot",
    "ilo_ip" : "192.168.56.10",
    "username" : "ilo_user",
    "password" : "ilo_password"
}
```

### disk boot

```json
{
    "sn" : "sn-xxx",
    "action" : "SetDiskBoot",
    "ilo_ip" : "192.168.56.10",
    "username" : "ilo_user",
    "password" : "ilo_password"
}
```

### power on

```json
{
    "sn" : "sn-xxx",
    "action" : "PowerOn",
    "ilo_ip" : "192.168.56.10",
    "username" : "ilo_user",
    "password" : "ilo_password"
 }
```

### power off

```json
{
    "sn" : "sn-xxx",
    "action" : "PowerOff",
    "ilo_ip" : "192.168.56.10",
    "username" : "ilo_user",
    "password" : "ilo_password"
}
```

### power reset

```json
{
    "sn" : "sn-xxx",
    "action" : "PowerReset",
    "ilo_ip" : "192.168.56.10",
    "username" : "ilo_user",
    "password" : "ilo_password"
}
```
