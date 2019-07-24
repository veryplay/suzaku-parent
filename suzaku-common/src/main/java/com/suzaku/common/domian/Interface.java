package com.suzaku.common.domian;

import lombok.Builder;
import lombok.Data;

import java.util.Date;

@Data
@Builder
public class Interface {

    private Long id;

    private String sn;

    private String name;

    private String type;

    private String mac;

    private String switchIp;

    private String switchPort;

    private Date createTime;

    private Date updateTime;

    private Boolean isDel;
}
