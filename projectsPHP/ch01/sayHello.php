<?php
	define('STDIN',fopen("php://stdin","r"));
	echo "Hello there, So I hear you're learning to be a PHP developer!\n";
	echo "Why don't you type your name for me:\n";
	$name = trim(fgets(STDIN));
	
	echo "\nThanks, " . $name . ", it's really nice to meet you.\n\n";
?>