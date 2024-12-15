<?php

use Illuminate\Support\Facades\Route;
use App\Livewire\Home\Index\Page AS HomePage;
use App\Livewire\Providers\Index\Page AS CourseProvidersPage;

Route::get('/', HomePage::class)->name('home.index');
Route::get('/providers', CourseProvidersPage::class)->name('providers.index');

Route::view('dashboard', 'dashboard')
    ->middleware(['auth', 'verified'])
    ->name('dashboard');

Route::view('profile', 'profile')
    ->middleware(['auth'])
    ->name('profile');

require __DIR__.'/auth.php';
