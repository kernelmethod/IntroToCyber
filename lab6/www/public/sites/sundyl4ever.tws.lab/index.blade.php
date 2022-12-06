@extends('default')

@php
$default_theme = 'Light';
@endphp

@section('site-title')
Sundyl4Ever
@endsection

@section('page-title')
<x-icon size=64 icon="heartbreak-fill" style="margin-right: 1em;"/>
RIP Sundyl... forever in our hearts
@endsection

@section('content')

<x-markdown>

Sorry everyone, but it's true... Sundyl is no more. We thought we could remain
solvent, but after we got hacked our sponsor abandoned us and we didn't have
enough money to last us through the rest of the year. &#x1f641;

We've set up this small page to memorialize Sundyl as our team moves on to
bigger and better things. Here are some of our favorite moments from our time
spent working on Sundyl:

</x-markdown>

<x-figure src="/sundyl_memorial_1.webp">
  <x-slot:caption>
Our website is live!
  </x-slot>
</x-figure>

<x-figure src="/sundyl_memorial_2.webp">
  <x-slot:caption>
Jodi yelling at Freddy for using the same password everywhere &#x1f923; I wonder
if he ever got around to changing it?
  </x-slot>
</x-figure>

<x-figure src="/sundyl_memorial_3.webp">
  <x-slot:caption>
We started getting our backend up and running. I was originally going to set up
Apache Airflow for this, but it turned out our machines didn't have enough
resources to support it!
  </x-slot>
</x-figure>

<x-figure src="/sundyl_memorial_4.webp">
  <x-slot:caption>
Freddy is on support duty! No matter the time of day, he is always quick to
provide help to those in need.
  </x-slot>
</x-figure>

<h2>Where are they now?</h2>

<div class="container" style="padding-bottom: 2em;">
  <div class="col text-center">
    <img class="portrait" style="max-height: 8em;" src="/kirby.webp">
  </div>
  <div class="col">
    <x-markdown>

_**Kirby Elledge:**_ it's me! For now I'm taking a break, I just wound down the
old Sundyl infrastructure and set up this page for all of our fellow sun dial
fans.

    </x-markdown>
  </div>
</div>

<div class="container" style="padding-bottom: 2em;">
  <div class="col text-center">
    <img class="portrait" style="max-height: 8em;" src="/jodi.webp">
  </div>
  <div class="col">
    <x-markdown>

_**Jodi Crockwell:**_ Jodi is off giving seminars at universities around the
country about the current state-of-the-art in password cracking. She just
started up a new consultancy for businesses looking to implement better password
policies for employees and users.

    </x-markdown>
  </div>
</div>

<div class="container" style="padding-bottom: 2em;">
  <div class="col text-center">
    <img class="portrait" style="max-height: 8em;" src="/freddy.webp">
  </div>
  <div class="col">
    <x-markdown>

_**Freddy Obrzut:**_ I'm actually not sure where Freddy is! The last time I
spoke with him he was muttering something about "cross-site scripting" and
getting revenge. Ah well, I'm sure he's doing fine -- maybe we'll see him again
sometime in the next few weeks. &#x1f642;

    </x-markdown>
  </div>
</div>

<div class="text-center">
  <x-icon icon="sun" style="padding: 2em;"/>
  <x-icon icon="sun" style="padding: 2em;"/>
  <x-icon icon="sun" style="padding: 2em;"/>
</div>

@endsection
