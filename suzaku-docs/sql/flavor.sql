drop table if exists flavor;

create table if not exists flavor(
    id bigint unsigned primary key auto_increment comment 'ID',
    code varchar(32) not null comment '规格',
    name varchar(32) not null comment '规格名称',
    family varchar(32) not null comment '规格类型compute/memory/storage',
    manufacturer_id bigint unsigned comment '产品id',
    extra_specs varchar(512) default null comment '额外信息',
    description varchar(256) comment '描述',
    create_time datetime not null comment '创建时间',
    update_time datetime default null comment '更新时间',
    is_del tinyint not null default 0 comment '是否删除(0-未删, 1-已删)'
) engine=innodb default charset=utf8 comment='规格';

create unique index uk_flavor_code on flavor(code);

