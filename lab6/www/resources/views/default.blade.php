@extends('base')

@php
$themes = [
  "Light" => Vite::asset('resources/css/lightmode.scss'),
  "Dark" => Vite::asset('resources/css/darkmode.scss'),
];
@endphp

{{-- Page navigation --}}
@section('navbar')
<a href="{{ URL::to('/'); }}" class="brand">
  <h2>
    @section('site-title')
    @show
  </h2>
</a>

<div class="pure-menu pure-menu-horizontal theme-selector">
  <ul class="pure-menu-list theme-selector-menu">
    <li class="pure-menu-item pure-menu-has-children pure-menu-allow-hover">
      <a href="#" id="menuLink1" class="pure-menu-link">Themes</a>
      <ul class="pure-menu-children">
      @foreach ($themes as $name => $uri)
      <li class="pure-menu-item">
        <a href="#" class="pure-menu-link" onclick="changeTheme('{{ $name }}')">
          {{ $name }}
        </a>
      </li>
      @endforeach
    </li>
  </ul>
</div>
@endsection

{{-- Additional stylesheets --}}
@push('stylesheets')
  @vite(['resources/css/lightmode.scss', 'resources/css/darkmode.scss'])
  <link type="text/css" rel="stylesheet" id="pageTheme">
@endpush

@push('scripts')
  <script type="module">
    function getConfiguredTheme() {
        return document.cookie
            .split('; ')
            .find((cookie) => cookie.startsWith('TICKTOCK_WHOST_THEME'))
            ?.split('=')[1];
    }

    // Set the theme in the user's cookies
    function setConfiguredTheme(themeName, themeMap) {
        document.cookie = `TICKTOCK_WHOST_THEME=${themeName}; SameSite=Strict;`;
    }

    // Set the page theme.
    function useTheme(themeName, defaultThemeName, themeMap) {
        let el = document.getElementById('pageTheme');
        let theme = themeMap.get(themeName);

        if (theme === undefined) {
            console.error(`Unknown theme ${themeName}. Defaulting to ${defaultThemeName}`);
            theme = themeMap.get(defaultThemeName);
        }
        el.href = theme;
    }

    const defaultThemeName = '{{ $default_theme ?? 'Dark' }}';
    const themeMap = new Map();
    @foreach ($themes as $name => $uri)
    themeMap.set('{{ $name }}', '{{ $uri }}');
    @endforeach

    let configuredTheme = getConfiguredTheme();

    if (configuredTheme === undefined) {
        configuredTheme = defaultThemeName;
        setConfiguredTheme(configuredTheme, themeMap);
    }

    useTheme(configuredTheme, defaultThemeName, themeMap);

    window.changeTheme = (name) => {
        setConfiguredTheme(name, themeMap);
        useTheme(name, defaultThemeName, themeMap);
    };
  </script>
@endpush

@section('content')
<section>

@isset($markdown)
<x-markdown>
  {!! $markdown !!}
</x-markdown>
@endisset

</section>
@endsection
