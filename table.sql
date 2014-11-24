create database statusdb default character set gbk;
use statusdb;
create table statustable (statusid int(11) not null auto_increment,conv_time datetime default null,offer_id varchar(20) default null,status varchar(10) default null,url varchar(1024) default null,PRIMARY KEY (statusid)) ENGINE=InnoDB DEFAULT CHARSET=gbk
create table offerstore (statusid int(11) not null auto_increment,conv_time datetime default null,offer_id varchar(20) default null, confirmed int(11) default null,accepted int(11) default null,diff int(11) default null,url varchar(255) default null,PRIMARY KEY (statusid)) ENGINE=InnoDB DEFAULT CHARSET=gbk;
create table advstore (statusid int(11) not null auto_increment,conv_time datetime default null,adv_id varchar(20) default null,url varchar(1024) default null,accepted int(11) default null,confirmed int(11) default null,diff int(11) default null,ip_whitelist varchar(4096) default null,isinym varchar(512) default null,isinhasofferwhiteiplist varchar(512) default null,PRIMARY KEY (statusid)) ENGINE=InnoDB DEFAULT CHARSET=gbk;
create table adv_offer (offer_id int, adv_id int, primary key(offer_id, adv_id)) ENGINE=InnoDB DEFAULT CHARSET=gbk;
create table advertiser (adv_id int, ip_whitelist varchar(1024), isinym varchar(512), isinhasofferwhiteiplist varchar(255), primary key (adv_id)) ENGINE=InnoDB DEFAULT CHARSET=gbk;
grant select,insert,update,delete,create,drop on statusdb.* to django@'%' identified by 'django';