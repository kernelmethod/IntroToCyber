<?php

date_default_timezone_set('UTC');
require 'vendor/s3.phar';

$s3 = new Aws\S3\S3Client([
  'version' => 'latest',
  'region' => 'us-east-1',
  'endpoint' => 'http://s3.ticktock.lab:9000',
  'use_path_style_endpoint' => true,
]);

// SDK docs: https://docs.aws.amazon.com/aws-sdk-php/v3/api/api-s3-2006-03-01.html#listobjects
$result = $s3->listObjects([
  'Bucket' => 'gallery',
]);

echo '<ul>';

foreach ($result["Contents"] as &$item) {
  $url = "/gallery/" . $item['Key'];
  $li = "<li>" . $item['Key'] . "</li>";
  echo "<a href='$url' target='_'>$li</a>";
}

echo "</ul>";

/*
$retrieve = $s3->getObject([
  "Bucket" => "gallery",
  "Key" => "grandfather_clock.jpg",
]);

echo $retrieve["Body"];
 */

?>
