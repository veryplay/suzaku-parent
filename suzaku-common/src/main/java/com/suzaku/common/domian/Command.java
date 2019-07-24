package com.suzaku.common.domian;

import lombok.Builder;
import lombok.Data;

import java.util.Date;

@Data
@Builder
public class Command {

    private Long id;

    private String requestId;

    private String sn;

    private String instanceId;

    private String action;

    private String type;

    private String status;

    private Long parentCommandId;

    private Integer executeCount;

    private Date createTime;

    private Date startTime;

    private Date updateTime;

    private Boolean isDel;

}
