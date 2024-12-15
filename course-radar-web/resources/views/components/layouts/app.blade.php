<!DOCTYPE html>
<html lang="{{ str_replace('_', '-', app()->getLocale()) }}">
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>{{ $title ?? 'Page Title' }}</title>
        @vite('resources/css/custom.css')
    </head>
    <body>
        <livewire:partials.main-navigation />
        {{ $slot }}
        @vite('resources/js/custom.js')
    </body>
</html>
