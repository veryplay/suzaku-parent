drop table if exists manufacturer;

create table if not exists manufacturer (
    id bigint unsigned primary key auto_increment comment 'ID',
    instacne_type varchar(32) not null comment '实例类型',
    manufacturer varchar(64) not null comment '厂商',    
    product_name varchar(128) not null comment '产品型号名称',
    create_time datetime not null comment '创建时间',
    update_time datetime default null comment '更新时间',
    is_del tinyint not null default 0 comment '是否删除：1删除，0未删除'
) engine=innodb default charset=utf8 comment='产品型号信息';