package com.suzaku.common.domian;

import lombok.Builder;
import lombok.Data;

import java.util.Date;

@Data
@Builder
public class OS {

    private Integer id;

    private String name;

    private String type;

    private String version;

    private String architecture;

    private Date createTime;

    private Date updateTime;

    private Boolean isDel;
}
