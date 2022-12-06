<?php

function nftcard($img, $title, $content, $price) {
  $url = "gallery/$img";

  echo <<<EOD
<div class="column col-6 nftcard">
  <div class="card">
    <div class="card-image">
      <a href="$url" target="_">
        <img src="$url" class="img-responsive gallery-img">
      </a>
    </div>
    <div class="card-header">
      <div class="card-title h5">$title</div>
    </div>
    <div class="card-body">
      $content
    </div>
    <div class="card-footer">
      <b>Price:</b> $price
    </div>
  </div>
</div>
EOD;
}

?>
