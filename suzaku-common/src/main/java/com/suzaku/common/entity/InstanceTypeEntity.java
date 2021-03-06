package com.suzaku.common.entity;

import lombok.Data;

import javax.persistence.*;
import java.util.Date;

@Entity
@Data
@Table(name = "instance_type")
public class InstanceTypeEntity {
    @Id
    @GeneratedValue(strategy= GenerationType.AUTO)
    private Integer id;

    private String code;

    private String name;

    private String family;

    private Integer manufacturerId;

    private String extraSpecs;

    private String description;

    @Column(updatable = false)
    @Temporal(TemporalType.TIMESTAMP)
    private Date createTime = new Date();

    @Temporal(TemporalType.TIMESTAMP)
    private Date updateTime;

    @Column(columnDefinition = "tinyint")
    private Boolean isDel = false;
}
