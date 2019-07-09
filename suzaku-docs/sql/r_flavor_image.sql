drop table if exists r_flavor_image;

create table if not exists r_flavor_image(
    id bigint unsigned primary key auto_increment comment 'ID',
    flavor varchar(32) not null comment '设备规格',
    image_id varchar(36) not null comment '镜像ID',
    create_time datetime not null comment '创建时间',
    update_time datetime default null comment '更新时间',
    is_del tinyint not null default 0 comment '是否删除(0-未删, 1-已删)'
) engine=innodb default charset=utf8 comment='设备支持镜像';

create index idx_r_flavor_image on r_flavor_image(flavor);
