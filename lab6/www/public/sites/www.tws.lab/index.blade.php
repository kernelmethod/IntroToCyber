@extends('default')

@section('site-title')
TickTock Web Hosting Platform
@endsection

@section('page-title')
<x-icon icon="cloud" width="100" height="100" style="margin-right: 1em;"/>
TickTock Web Hosting
@endsection

@section('content')
<x-markdown>

For years, our customers have counted on us to get the most up-to-date time measurements
at nanosecond precision, and to connect them with time professionals throughout the
world.

Now you can run your own website with the same speed and global reach as
TickTock, thanks to our brand-new web services division. Whether you're setting
up a blog or starting a business, you can rely on TickTock's infrastructure to
deliver your pages on time.

</x-markdown>

<div class="text-center">
<h3>A product of TickTock Global Platforms, Inc.</h3>
</div>

<div class="separator"></div>

<section>
  <div class="container">

<div class="col card-img">
<x-icon icon="clock-history"/>
</div>

<div class="col">

<x-markdown>

## Blazing fast

You've never seen PHP pages served so quickly before.

**Think you have?** Wrong. You haven't.

</x-markdown>

</div>
</div>
</section>

<div class="separator"></div>

<section>
<div class="container">
<div class="col" style="text-align: right;">

<x-markdown>

## We will run anything

Send us your absolute worst code. We will run it.

**Remote code execution?** Sounds like fun!

</x-markdown>

</div>
<div class="col card-img">
<x-icon icon="filetype-php"/>
</div>
</div>
</section>

<div class="separator"></div>

<section>
<div class="container">

<div class="col card-img">
<x-icon icon="patch-check"/>
</div>
<div class="col">

<x-markdown>

## Get one of these cool checkmarks for your site</h2>

Looks nice, right? Apparently it comes with [Bootstrap's](https://getbootstrap.com)
icon set.

**Starting at $8 / month**

</x-markdown>

</div>

</div>
</section>

<div class="separator"></div>

<section>
<div class="container">
<div class="col" style="text-align: right;">

<x-markdown>

## Secure, probably.

Look, we don't really know, but we recently hired somebody who hacked us a bunch
of times to implement something called "application armor".

**Sounds legit to us.**

</x-markdown>
</div>

<div class="col card-img">
<x-icon icon="shield-lock"/>
</div>

</div>
</section>

<div class="separator"></div>

<section>
<div class="container">
<div class="col card-img">

<x-icon icon="currency-bitcoin"/>

</div>
<div class="col">

<x-markdown>

## Now accepting Bitcoin

Check out our NFT gallery, too!

</x-markdown>

</div>
</div>
</section>

@endsection
