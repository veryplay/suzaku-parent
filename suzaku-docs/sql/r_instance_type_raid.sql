drop table if exists r_instance_type_raid;

create table if not exists r_instance_type_raid(
    id bigint unsigned primary key auto_increment comment 'ID',
    instacne_type varchar(16) not null comment '实例类型',
    raid_level varchar(36) not null comment 'raid',
    volume_type varchar(16) not null comment '磁盘类型 root/data',
    create_time datetime not null comment '创建时间',
    update_time datetime default null comment '更新时间',
    is_del tinyint not null default 0 comment '是否删除(0-未删, 1-已删)'
) engine=innodb default charset=utf8 comment='设备支持的raid';

create index idx_r_instacne_type_raid_level on r_instance_type_raid(instacne_type, raid_level);