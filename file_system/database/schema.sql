CREATE TABLE PasteFile(
  id int(11) NOT NULL AUTO_INCREMENT,
  filename varchar(5000) NOT null,
  filehash varchar(128) NOT null,
  filemd5 varchar(128) NOT null,
  uploadtime datetime NOT null,
  mimetype varchar(256) NOT null,
  size int(11) unsigned NOT NULL,
  PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



