drop table if exists raid;

create table if not exists raid(
    id bigint unsigned primary key auto_increment comment 'ID',
    raid_level varchar(16) not null comment 'raid',
    description varchar(512) comment '描述',
    create_time datetime not null comment '创建时间',
    update_time datetime default null comment '更新时间',
    is_del tinyint not null default 0 comment '是否删除(0-未删, 1-已删)'
) engine=innodb default charset=utf8 comment='raid';
