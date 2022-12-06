{{-- Laravel component for figures --}}

@props(['alt' => '', 'src', 'caption'])

<figure {{ $attributes }}>
  <img src="{{ $src }}" alt="{{ $alt }}">

  @isset($caption)
  <figcaption>
    {{ $caption }}
  </figcaption>
  @endisset
</figure>
