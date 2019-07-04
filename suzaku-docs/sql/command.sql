drop table if exists command;

create table if not exists command(
    id bigint unsigned primary key auto_increment comment 'ID',
    request_id varchar(64) not null comment '请求ID',
    sn varchar(64) not null comment '设备SN',
    instance_id varchar(36) comment '实例Id',
    action varchar(32) not null comment '操作',
    type varchar(16) not null comment '操作类型：agent, driver, network',    
    status varchar(16) comment '状态: wait,running,finish,error,cancel',
    parent_command_id bigint unsigned comment '父指令Id',
    execute_count int unsigned not null comment '执行次数',
    create_time datetime not null comment '创建时间',
    start_time datetime default null comment '开始执行时间',
    update_time datetime default null comment '更新时间',
    is_del tinyint not null default 0 comment '是否删除(0-未删, 1-已删)'
) engine=innodb default charset=utf8 comment='指令';

create index idx_command_request_id on command(request_id);
create index idx_command_sn on command(sn);
create index idx_command_instance_id on command(instance_id);