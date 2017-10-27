BEGIN TRANSACTION;
CREATE TABLE "outlet" (
	`alias`	TEXT NOT NULL,
	`number`	INTEGER NOT NULL,
	`userAlias`	TEXT NOT NULL
);
INSERT INTO "outlet" VALUES('promo-9192-banners',2288416,'promo-9193');
INSERT INTO "outlet" VALUES('promo-9293',2156999,'promo-9193');
INSERT INTO "outlet" VALUES('promo-9193-coupons',2288416,'promo-9193');
INSERT INTO "outlet" VALUES('promo-9293',2156999,'promo-9193');
INSERT INTO "outlet" VALUES('promo-80',2743206,'promo-1075');
INSERT INTO "outlet" VALUES('promo-93',5772504,'promo-9193');
INSERT INTO "outlet" VALUES('cds-9193',5116821,'cds');
INSERT INTO "outlet" VALUES('cds-off-fo',1137767,'admycca');
INSERT INTO "outlet" VALUES('promo-1030-92',1148617,'promo-1075');
INSERT INTO "outlet" VALUES('promo-50',2156416,'promo-1075');
INSERT INTO "outlet" VALUES('promo-60',2156672,'promo-1075');
INSERT INTO "outlet" VALUES('promo-70',2270933,'promo-1075');
INSERT INTO "outlet" VALUES('promo-40
',2743206,'promo-1075');
INSERT INTO "outlet" VALUES('promo-1020-91',5204048,'promo-1075');
INSERT INTO "outlet" VALUES('cds-on-fo',5772504,'admycca');
INSERT INTO "outlet" VALUES('cds-80',5101222,'cds');
INSERT INTO "outlet" VALUES('pay-access',1148617,'corin');
INSERT INTO "outlet" VALUES('freq-ordered',8000353,'payment-access');
INSERT INTO "outlet" VALUES('freq-ordered2',100036,'payment-access');
CREATE TABLE "user" (
	`alias`	TEXT,
	`username`	TEXT,
	`password`	TEXT,
	PRIMARY KEY(`username`)
);
INSERT INTO "user" VALUES('promo-9193','cutedog@xyz123.com','35Paxton');
INSERT INTO "user" VALUES('payment-access','abcdxyz@outlook.com','Mycca@11');
INSERT INTO "user" VALUES('promo-1075','myccatest123@gmail.com','Mycca@11');
INSERT INTO "user" VALUES('webtestuser','webtestuser1','b');
INSERT INTO "user" VALUES('admin-bde','admycca@outlook.com','Mycca@11');
INSERT INTO "user" VALUES('corin','corin3@hotmail.com','Coke@123');
INSERT INTO "user" VALUES('testcust','testcustomercca@outlook.com','Mycca@15');
COMMIT;
