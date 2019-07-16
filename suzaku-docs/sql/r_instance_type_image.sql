drop table if exists r_instance_type_image;

create table if not exists r_instance_type_image(
    id bigint unsigned primary key auto_increment comment 'ID',
    instacne_type varchar(16) not null comment '实例类型',
    image_id varchar(36) not null comment '镜像ID',
    create_time datetime not null comment '创建时间',
    update_time datetime default null comment '更新时间',
    is_del tinyint not null default 0 comment '是否删除(0-未删, 1-已删)'
) engine=innodb default charset=utf8 comment='实例类型与镜像关联关系';

create index idx_r_instance_type_image_instacne_type on r_instance_type_image(instacne_type);
