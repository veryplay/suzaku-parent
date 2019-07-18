drop table if exists interface;

create table if not exists interface(
    id bigint unsigned primary key auto_increment comment 'ID',
    sn varchar(32) not null comment '设备SN',
    name varchar(16) not null comment '网卡名称',
    type varchar(16) not null comment '网卡类型：lan/wan',
    mac varchar(32) not null comment 'MAC',
    switch_ip varchar(32) not null comment '上联交换机IP',
    switch_port varchar(32) not null comment '上联交换机Port',
    create_time datetime not null comment '创建时间',
    update_time datetime default null comment '更新时间',
    is_del tinyint not null default 0 comment '是否删除(0-未删。1-已删)'
) engine=innodb default charset=utf8 comment='网卡信息';

create index idx_interface_sn on interface(sn);
