{{-- Laravel component for rendering a Bootstrap icon --}}

@props(['size' => 100, 'icon'])

<svg class="bi" fill="currentColor"
  @isset($size) width="{{ $size }}" height="{{ $size }}" @endisset
  {{ $attributes }}>
  <use xlink:href="/bootstrap-icons.svg#{{ $icon }}">
</svg>
