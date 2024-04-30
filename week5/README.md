## TASK 2
- CREATE DATABASE \`website\`;
<img src="./Screenshot/TASK 2/TASK2-1.jpg">TASK2-1</img>
- CREATE TABLE \`member\`(\`id\` BIGINT PRIMARY KEY AUTO_INCREMENT,\`name\` VARCHAR(255) NOT NULL, \`username\` VARCHAR(255) NOT NULL, \`password\` VARCHAR(255) NOT  NULL, \`follower_count\` INT UNSIGNED NOT NULL DEFAULT 0, \`time\` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP);<br>DESCRIBE \`member\`;
<img src="./Screenshot/TASK 2/TASK2-2.jpg">TASK2-2</img>
## TASK 3
- INSERT INTO \`member\`(\`name\`,\`username\`,\`password\`,\`follower_count\`) VALUES("test","test","test", 0);<br>INSERT INTO \`member\`(\`name\`,\`username\`,\`password\`,\`follower_count\`) VALUES("小明","user001","123456", 500); <br>INSERT INTO \`member\`(\`name\`,\`username\`,\`password\`,\`follower_count\`) VALUES("小美","user002","321123", 1000);<br>INSERT INTO \`member\`(\`name\`,\`username\`,\`password\`,\`follower_count\`) VALUES("小白","user003","11112222", 1200);<br>INSERT INTO \`member\`(\`name\`,\`username\`,\`password\`,\`follower_count\`) VALUES("小黑","user004","22221111", 800);
<img src="./Screenshot/TASK 3/TASK3-1.jpg">TASK3-1</img>
## TASK 4
## TASK 5
