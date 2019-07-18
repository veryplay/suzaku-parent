drop table if exists image;

create table if not exists image(
    id bigint unsigned primary key auto_increment comment 'ID',
    uuid varchar(36) not null comment '镜像ID',
    name varchar(32) not null comment '中文名',
    version varchar(16) comment '镜像版本',
    os_id int not null comment '操作系统ID',
    format varchar(16) not null comment '镜像格式',
    filename varchar(64) not null comment '镜像文件名称',
    url varchar(256) not null comment '镜像源路径',
    hash varchar(128) not null comment '镜像校验码',
    description varchar(256) comment '描述',
    create_time datetime not null comment '创建时间',
    update_time datetime default null comment '更新时间',
    is_del tinyint not null default 0 comment '是否删除(0-未删, 1-已删)'
) engine=innodb default charset=utf8 comment='镜像';

create unique index uk_image_uuid on image(uuid);
create index idx_image_os_id on image(os_id);

