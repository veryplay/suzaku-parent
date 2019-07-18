create table if not exists os(
    id int unsigned primary key auto_increment comment 'ID',
    name varchar(16) not null comment '操作系统名称',
    type varchar(16) not null comment '操作系统分类:ubuntu/centos/windows',
    version varchar(16) not null comment '操作系统版本',
    architecture varchar(16) not null comment '架构:x86/x64/i386/',
    create_time datetime not null comment '创建时间',
    update_time datetime default null comment '更新时间',
    is_del tinyint not null default 0 comment '是否删除(0-未删, 1-已删)'
) engine=innodb default charset=utf8 comment='os';

drop table if exists os;

create unique index uk_os_uuid on os(uuid);


