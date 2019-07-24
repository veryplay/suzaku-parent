package com.suzaku.common.domian;

import lombok.Builder;
import lombok.Data;

import java.util.Date;

@Data
@Builder
public class Manufacturer {

    private Integer id;

    private String instanceType;

    private String manufacturer;

    private String productName;

    private Date createTime;

    private Date updateTime;

    private Boolean isDel;
}
