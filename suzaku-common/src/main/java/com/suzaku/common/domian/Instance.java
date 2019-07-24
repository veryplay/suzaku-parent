package com.suzaku.common.domian;

import lombok.Builder;
import lombok.Data;

import java.util.Date;

@Data
@Builder
public class Instance {

    private Long id;

    private String uuid;

    private String sn;

    private String tenant;

    private String name;

    private String hostname;

    private String imageId;

    private String rootVolumeRaidLevel;

    private String dataVolumeRaidLevel;

    private String privateIp;

    private String publicIp;

    private String status;

    private String description;

    private Date createTime;

    private Date updateTime;

    private Boolean isDel;
}
