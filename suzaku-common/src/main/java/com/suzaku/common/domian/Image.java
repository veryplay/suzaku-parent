package com.suzaku.common.domian;

import lombok.Builder;
import lombok.Data;

import java.util.Date;

@Data
@Builder
public class Image {
    private Integer id;

    private String uuid;

    private String name;

    private String version;

    private Integer osId;

    private String format;

    private String filename;

    private String url;

    private String hash;

    private String description;

    private Date createTime;

    private Date updateTime;

    private Boolean isDel;
}
