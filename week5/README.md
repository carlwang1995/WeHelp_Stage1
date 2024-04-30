## TASK 2
- CREATE DATABASE \`website\`;
<img src="./Screenshot/TASK 2/TASK2-1.jpg">上圖：TASK2-1</img>
- USE \`website\`;<br>CREATE TABLE \`member\`(<br>　\`id\` BIGINT PRIMARY KEY AUTO_INCREMENT,<br>　\`name\` VARCHAR(255) NOT NULL,<br>　\`username\` VARCHAR(255) NOT NULL,<br>　\`password\` VARCHAR(255) NOT  NULL,<br>　\`follower_count\` INT UNSIGNED NOT NULL DEFAULT 0,<br>　\`time\` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP<br>);<br>DESCRIBE \`member\`;
<img src="./Screenshot/TASK 2/TASK2-2.jpg">上圖：TASK2-2</img>
## TASK 3
- INSERT INTO \`member\`(\`name\`,\`username\`,\`password\`,\`follower_count\`) VALUES("test","test","test", 0);<br>INSERT INTO \`member\`(\`name\`,\`username\`,\`password\`,\`follower_count\`) VALUES("小明","user001","123456", 500); <br>INSERT INTO \`member\`(\`name\`,\`username\`,\`password\`,\`follower_count\`) VALUES("小美","user002","321123", 1000);<br>INSERT INTO \`member\`(\`name\`,\`username\`,\`password\`,\`follower_count\`) VALUES("小白","user003","11112222", 1200);<br>INSERT INTO \`member\`(\`name\`,\`username\`,\`password\`,\`follower_count\`) VALUES("小黑","user004","22221111", 800);
<img src="./Screenshot/TASK 3/TASK3-1.jpg">上圖：TASK3-1</img>
- SELECT * FROM \`member\`;
<img src="./Screenshot/TASK 3/TASK3-2.jpg">上圖：TASK3-2</img>
- SELECT * FROM \`member\` ORDER BY \`time\` DESC;
<img src="./Screenshot/TASK 3/TASK3-3.jpg">上圖：TASK3-3</img>
- SELECT * FROM \`member\` ORDER BY \`time\` DESC LIMIT 1,3;
<img src="./Screenshot/TASK 3/TASK3-4.jpg">上圖：TASK3-4</img>
- SELECT * FROM \`member\` WHERE \`username\` = "test";
<img src="./Screenshot/TASK 3/TASK3-5.jpg">上圖：TASK3-5</img>
- SELECT * FROM \`member\` WHERE \`name\` LIKE "%es%" OR "es%" OR "%es";
<img src="./Screenshot/TASK 3/TASK3-6.jpg">上圖：TASK3-6</img>
- SELECT * FROM \`member\` WHERE \`username\` = "test" AND \`password\` = "test";
<img src="./Screenshot/TASK 3/TASK3-7.jpg">上圖：TASK3-7</img>
- UPDATE \`member\` SET \`name\` = "test2" WHERE \`username\` = "test";
<img src="./Screenshot/TASK 3/TASK3-8.jpg">上圖：TASK3-8</img>
## TASK 4
- SELECT COUNT(*) FROM \`member\`;
<img src="./Screenshot/TASK 4/TASK4-1.jpg">上圖：TASK4-1</img>
- SELECT SUM(\`follower_count\`) FROM \`member\`;
<img src="./Screenshot/TASK 4/TASK4-2.jpg">上圖：TASK4-2</img>
- SELECT AVG(\`follower_count\`) FROM \`member\`;
<img src="./Screenshot/TASK 4/TASK4-3.jpg">上圖：TASK4-3</img>
- SELECT AVG(\`follower_count\`) FROM (SELECT \`follower_count\` FROM \`member\` ORDER BY \`follower_count\` DESC LIMIT 2) AS \`subquery_alias\`;
<img src="./Screenshot/TASK 4/TASK4-4.jpg">上圖：TASK4-4</img>
## TASK 5
- CREATE TABLE \`message\`(<br>　\`id\` BIGINT PRIMARY KEY AUTO_INCREMENT,<br>　\`member_id\` BIGINT NOT NULL,<br>　\`content\` VARCHAR(255) NOT NULL,<br>　\`like_count\` INT UNSIGNED NOT NULL DEFAULT 0,<br>　\`time\` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,<br>　FOREIGN KEY(\`member_id\`) REFERENCES \`member\`(\`id\`) ON DELETE CASCADE<br>);<br>
DESCRIBE \`message\`;
<img src="./Screenshot/TASK 5/TASK5-1.jpg">上圖：TASK5-1</img>
- SELECT \`message\`.*, \`member\`.\`name\` FROM \`message\` JOIN \`member\` ON \`message\`.\`member_id\` = \`member\`.\`id\` ;
<img src="./Screenshot/TASK 5/TASK5-2.jpg">上圖：TASK5-2</img>
- SELECT \`message\`.*, \`member\`.\`name\` FROM \`message\` JOIN \`member\` ON \`message\`.\`member_id\` = \`member\`.\`id\` WHERE \`member\`.\`username\` = "test";
<img src="./Screenshot/TASK 5/TASK5-3.jpg">上圖：TASK5-3</img>
- SELECT AVG(\`like_count\`) FROM \`message\` JOIN \`member\` ON \`message\`.\`member_id\` = \`member\`.\`id\` WHERE \`member\`.\`username\` = "test";
<img src="./Screenshot/TASK 5/TASK5-4.jpg">上圖：TASK5-4</img>
- SELECT AVG(\`like_count\`) FROM \`message\` JOIN \`member\` ON \`message\`.\`member_id\` = \`member\`.\`id\` GROUP BY \`member\`.\`username\`;
<img src="./Screenshot/TASK 5/TASK5-5.jpg">上圖：TASK5-5</img>
