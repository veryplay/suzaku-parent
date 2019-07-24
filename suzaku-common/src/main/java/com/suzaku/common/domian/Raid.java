package com.suzaku.common.domian;

import lombok.Data;

import java.util.Date;

@Data
public class Raid {

    private Integer id;

    private String raidLevel;

    private String description;

    private Date createTime;

    private Date updateTime;

    private Boolean isDel;
}
