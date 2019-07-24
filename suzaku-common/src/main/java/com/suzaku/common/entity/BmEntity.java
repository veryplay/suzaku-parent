package com.suzaku.common.entity;

import lombok.Data;

import javax.persistence.*;
import java.util.Date;

@Entity
@Data
@Table(name = "bm")
public class BmEntity {

    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
    private Long id;

    private String sn;

    private String instanceType;

    private String iloIp;

    private String cabinet;

    private String uPosition;

    private String status;

    private String remark;

    @Column(updatable = false)
    @Temporal(TemporalType.TIMESTAMP)
    private Date createTime = new Date();

    @Temporal(TemporalType.TIMESTAMP)
    private Date updateTime;

    @Column(columnDefinition = "tinyint")
    private Boolean isDel = false;

}

