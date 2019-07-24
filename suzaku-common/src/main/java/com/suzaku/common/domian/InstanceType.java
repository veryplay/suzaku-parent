package com.suzaku.common.domian;

import lombok.Builder;
import lombok.Data;

import java.util.Date;

@Data
@Builder
public class InstanceType {

    private Integer id;

    private String code;

    private String name;

    private String family;

    private Integer manufacturerId;

    private String extraSpecs;

    private String description;

    private Date createTime;

    private Date updateTime;

    private Boolean isDel;
}
