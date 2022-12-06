<!doctype html>
<?php
include "includes/functions.php";
?>
<html lang="en-US">
  <head>
    <title>TickTock NFT Gallery</title>
    <meta name="description" content="TickTock NFT Gallery">
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link rel="stylesheet" href="https://unpkg.com/spectre.css/dist/spectre.min.css">
    <link rel="stylesheet" href="/static/site.css">
  </head>

  <body>
    <header class="navbar bg-secondary">
      <section class="navbar-section">
        <a href="/" class="navbar-brand mr-2">
          <h1>TickTock NFT Gallery</h1>
        </a>
      </section>
    </header>

    <div class="columns">

      <?php
        nftcard(
          "grandfather_clock.jpg",
          "Wow, look at this clock!",
          "very beautiful, very powerful",
          "5 ETH"
        );
      ?>

      <?php
        nftcard(
          "fancy_clock.jpg",
          "ooh, fancy!",
          "so shiny... so intricate... it really makes you want to buy a JPEG of a clock",
          "3 BTC"
        );
      ?>

      <?php
        nftcard(
          "nautical_clock.jpg",
          "ahoy! this one kind of looks like a ship",
          "it even has an anchor!",
          "0.7 YAR"
        );
      ?>

      <?php
        nftcard(
          "serene_clock.jpg",
          "this clock is very calming to look at",
          "you could look at it too if you bought this nft",
          "100 elon bux"
        );
      ?>

    </div>

    <div class="bg-dark p-2">
      <h2>Interested in buying one of these NFTs?</h2>
      <h3>
        Contact the site administrator at admin@ticktock.lab for more information!*
      </h3>
      <div class="text-italic" style="margin-top: 512px;">
        <p>
          *NOTE: this is not a real email address, these are not actual NFTs,
          and everything on this page is satirical. :)
        </p>
      </div>
    </div>

  </body>
</html>
