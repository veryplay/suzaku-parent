drop table if exists instance;

create table if not exists instance(
    id bigint unsigned primary key auto_increment comment 'ID',
    uuid varchar(36) not null comment '实例ID',
    sn bigint unsigned not null comment '设备sn',
    tenant varchar(64) not null comment '租户',
    name varchar(136) comment '实例名称',
    hostname varchar(72) comment '主机名',
    image_id varchar(36) not null comment '镜像ID',
    root_volume_raid_level varchar(36) comment '系统盘raid',
    data_volume_raid_level varchar(36) comment '数据盘raid',
    private_ip varchar(32) comment '内网ip',
    public_ip varchar(32) comment '公网IP',
    status varchar(16) not null comment '实例状态',
    description varchar(256) comment '描述',
    create_time datetime not null comment '创建时间',
    update_time datetime default null comment '更新时间',
    is_del tinyint unsigned not null default 0 comment '是否删除(0-未删, 1-已删)'
) engine=innodb default charset=utf8 comment='实例';

create unique index uk_instance_uuid on instance(uuid);
create index idx_instance_tenant on instance(tenant);
create index idx_instance_sn on instance(sn);