package com.suzaku.common.domian;

import lombok.Builder;
import lombok.Data;

import java.util.Date;

@Data
@Builder
public class Bm {

    private Long id;

    private String sn;

    private String instanceType;

    private String iloIp;

    private String cabinet;

    private String uPosition;

    private String status;

    private String remark;

    private Date createTime;

    private Date updateTime;

    private Boolean isDel;
}
