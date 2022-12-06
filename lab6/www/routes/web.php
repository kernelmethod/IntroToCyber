<?php

use Illuminate\Support\Facades\Blade;
use Illuminate\Support\Facades\Route;
use Illuminate\Support\Facades\Redirect;
use Illuminate\Support\Facades\Log;

/*
|--------------------------------------------------------------------------
| Web Routes
|--------------------------------------------------------------------------
|
| Here is where you can register web routes for your application. These
| routes are loaded by the RouteServiceProvider within a group which
| contains the "web" middleware group. Now create something great!
|
*/

if (!function_exists('render_page')) {
    function render_page($page) {
        $site_files = public_path() . "/sites/" . request()->getHost();
        $host = request()->getHost();
        Log::error("Host = $host");

        // Render page as markdown
        $md_path = $site_files . "/$page.md";
        Log::error("Trying to find $md_path");
        if (file_exists($md_path)) {
            $markdown = file_get_contents($md_path);
            return view('default', ['markdown' => $markdown]);
        }

        // Render page as a Blade template
        $blade_path = $site_files . "/${page}.blade.php";
        if (file_exists($blade_path)) {
            $php = file_get_contents($blade_path);
            return Blade::render($php);
        }

        return view('default');

        // Page does not exist; return a 404
        Log::error("Could not find page $page");
        return response()->view('404')->setStatusCode(404);
    }
}

// Route::redirect('/', '/home');

Route::get('/', function () {
    $host = request()->getHost();
    Log::error("Host = $host");
    return render_page('index');
});

/*
Route::get('/{page}', function ($page) {
    return render_page($page);
});
 */
