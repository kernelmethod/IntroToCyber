<!doctype html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
  <head>
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1">

    <title>
    @section('site-title')
    @show
    </title>

    <!-- Fonts -->
    <link href="https://fonts.googleapis.com/css2?family=Nunito:wght@400;600;700&display=swap" rel="stylesheet">

    @vite([
      'resources/css/site.css',
      'resources/css/normalize.css',
      'resources/css/pure-min.css',
      'resources/js/themes.js'
    ])
    @stack('stylesheets')
  </head>

  <body>
    <nav class="container container-align">
      @section('navbar')
      @show
    </nav>

    <main>
      <header class="page-title">
        <h1 class="container container-align">
          @section('page-title')
          @show
        </h1>
      </header>

      <article>
        @section('content')
        @show
      </article>
    </main>

    <footer>
      <div class="container text-light" style="margin-bottom: 2em;">
        <div class="col">
        @php
        $home = getenv('HOSTNAME');
        @endphp
          This page was served by
          <a href="{{ $home }}">TickTock Web Services</a>, a product of TickTock Global
          Platforms, Inc.
        </div>
        <div class="col">
          <div class="col" style="text-align: right;">
            Built with <a href="https://laravel.com/">Laravel</a>
          </div>
        </div>
      </div>
      <div class="container">
        <div class="col text-light text-italic render-results">
          This page took  {{ round(microtime(true) - LARAVEL_START, 4) }} seconds to render
        </div>
      </div>
    </footer>
  </body>

  @stack('scripts')
</html>
