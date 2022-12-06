import { defineConfig } from 'vite';
import laravel from 'laravel-vite-plugin';

export default defineConfig({
    plugins: [
        laravel({
            input: [
                'resources/css/site.css',
                'resources/css/lightmode.scss',
                'resources/css/darkmode.scss',
                'resources/css/normalize.css',
                'resources/css/pure-min.css',
                'resources/js/app.js',
                'resources/js/themes.js',
                'resources/js/showdown/showdown.min.js',
            ],
            refresh: true,
        }),
    ],
});
