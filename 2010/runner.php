#!/usr/bin/php
<?php
$width = 1024;
$height = 768;
$timeout = 10;

$DB = unserialize(file_get_contents('./data.db'));

foreach ($DB as $t) {
  print_r($t);
  $cmd = "./webkit2png.py -x -g $width $height -o ./caps/".$t[1]."/".
    	   $t[1]." -t $timeout ".$t[2]." --debug -d ".(50+$i++);
  exec($cmd);
  unset($DB['$id']);
}

file_put_contents('./data.db', serialize($DB));