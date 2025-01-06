<?php

use Illuminate\Support\Facades\Route;
use App\Livewire\Home\Index\Page AS HomePage;
use App\Livewire\Providers\Index\Page AS CourseProvidersPage;
use App\Livewire\Courses\Index\Page AS CoursesPage;
use App\Livewire\Courses\Permalink\Page AS CoursePermalinkPage;

Route::get('/', HomePage::class)->name('home.index');
Route::get('/providers', CourseProvidersPage::class)->name('providers.index');

Route::name('courses.')
    ->prefix('/courses')
    ->group(function () {
        Route::get('/', CoursesPage::class)->name('index');
        Route::get('/{course}', CoursePermalinkPage::class)
            ->where('course', '^[1-9][0-9]*$')->name('permalink');
    });

Route::view('dashboard', 'dashboard')
    ->middleware(['auth', 'verified'])
    ->name('dashboard');

Route::view('profile', 'profile')
    ->middleware(['auth'])
    ->name('profile');

require __DIR__.'/auth.php';
