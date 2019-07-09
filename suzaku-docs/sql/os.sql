drop table if exists os;

create table if not exists os(
    id bigint unsigned primary key auto_increment comment 'ID',
    uuid varchar(36) not null comment '操作系统ID',
    name varchar(16) not null comment '操作系统名称',
    type varchar(16) not null comment '操作系统分类:ubuntu/centos/windows',
    architecture varchar(16) not null comment '架构:x86/x64/i386/',
    version varchar(16) not null comment '操作系统版本',
    create_time datetime not null comment '创建时间',
    update_time datetime default null comment '更新时间',
    is_del tinyint not null default 0 comment '是否删除(0-未删, 1-已删)'
) engine=innodb default charset=utf8 comment='os';

create unique index uk_os_uuid on os(uuid);


