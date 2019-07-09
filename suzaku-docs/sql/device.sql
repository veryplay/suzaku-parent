drop table if exists device;

create table if not exists device(
    id bigint unsigned primary key auto_increment comment '设备ID编号',
    sn varchar(64) not null comment '设备SN',
    flavor varchar(16) not null comment '规格',
    ilo_ip varchar(32) comment '带外管理IP',
    cabinet varchar(64) comment '机柜编号',
    u_position varchar(64) comment 'U位',
    status varchar(16) comment '状态',
    remark varchar(256) comment '备注',
    create_time datetime not null comment '创建时间',
    update_time datetime default null comment '更新时间',
    is_del tinyint not null default 0 comment '是否删除(0-未删, 1-已删)'
) engine=innodb default charset=utf8 comment='设备信息';

create unique index ux_device_sn on device(sn);