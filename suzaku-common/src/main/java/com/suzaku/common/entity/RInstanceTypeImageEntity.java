package com.suzaku.common.entity;

import lombok.Data;

import javax.persistence.*;
import java.util.Date;

@Entity
@Data
@Table(name = "r_instance_type_image")
public class RInstanceTypeImageEntity {
    @Id
    @GeneratedValue(strategy= GenerationType.AUTO)
    private Integer id;

    private String instanceType;

    private String imageId;

    @Column(updatable = false)
    @Temporal(TemporalType.TIMESTAMP)
    private Date createTime = new Date();

    @Temporal(TemporalType.TIMESTAMP)
    private Date updateTime;

    @Column(columnDefinition = "tinyint")
    private Boolean isDel = false;
}
