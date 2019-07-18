package com.suzaku.common.entity;

import lombok.Data;

import javax.persistence.*;
import java.util.Date;

@Entity
@Data
@Table(name = "instance")
public class InstanceEntity {
    @Id
    @GeneratedValue(strategy = GenerationType.AUTO)
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

    @Column(updatable = false)
    @Temporal(TemporalType.TIMESTAMP)
    private Date createTime = new Date();

    @Temporal(TemporalType.TIMESTAMP)
    private Date updateTime;

    @Column(columnDefinition = "tinyint")
    private Boolean isDel = false;
}
