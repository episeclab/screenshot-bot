<?php
//file_put_contents('/tmp/'.$_SERVER['REMOTE_ADDR'], print_r($_SERVER, true));

$width = 1024;
$height = 768;
$timeout = 30;

chdir('/home/esl/screen');

//print_r(scandir('.'));
$url = substr($_SERVER['REQUEST_URI'], strlen('/get/'));
$p = parse_url($url);

//print_r($p);
$dir = trim(preg_replace('/--*/', '-', preg_replace('@[^a-zA-Z0-9_-]@', '-', $p['host'])), '-');
@mkdir("./caps/$dir");
$id = preg_replace('/[^a-zA-Z0-9-]/', '', $url).'_'.time().'.png';



//if ($_SERVER['REMOTE_ADDR'] == '127.0.0.1') {
//   header('Connection: close');

$cmd = "./webkit2png.py -x -g $width $height -o ./caps/$dir/$id -t $timeout $url --debug";
//echo $cmd."<br/><br/>";
exec($cmd." > /dev/null 2>&1 & echo $!");
//exec($cmd);

//} else {
//$cmd = 'curl -s -I "http://localhost'.$_SERVER['REQUEST_URI'].'" >/dev/null &';
//echo $cmd;
//system($cmd);
//curl_exec($c);
//$fd = fsockopen('localhost', 80);
//fwrite($fd, "GET ".$_SERVER['REQUEST_URI']." HTTP/1.1\r\nHost: screener.esl\r\n\r\n");
//sleep(1);
//fclose($fd);
  echo "http://petitchien.esl/$dir/$id";
//}
