{{-- Laravel component to define a region that contains Markdown content --}}

{{-- Generate a random ID for the element containing Markdown --}}
@php
  $el_id = uniqid();
@endphp

@once
  @push('scripts')
    <script src="https://cdnjs.cloudflare.com/ajax/libs/showdown/2.1.0/showdown.min.js" integrity="sha512-LhccdVNGe2QMEfI3x4DVV3ckMRe36TfydKss6mJpdHjNFiV07dFpS2xzeZedptKZrwxfICJpez09iNioiSZ3hA==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
  @endpush
@endonce

@push('scripts')
<script defer>
  (() => {
    let id = "{{ $el_id }}";
    let converter = new showdown.Converter();
    let el_md = document.getElementById("md-" + id);
    let el_html = document.getElementById("final-" + id);
    let html = converter.makeHtml(el_md.innerText);
    el_md.parentNode.removeChild(el_md);
    el_html.innerHTML = html;
  })();
</script>
@endpush

{{-- Markdown content --}}
<pre id="md-{{ $el_id }}">{{ $slot }}</pre>
<div id="final-{{ $el_id }}"></div>
