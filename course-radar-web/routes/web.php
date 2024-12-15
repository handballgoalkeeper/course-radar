<?php

use Illuminate\Support\Facades\Route;
use App\Livewire\Home\Index\Page AS HomePage;

Route::get('/', HomePage::class);

Route::view('dashboard', 'dashboard')
    ->middleware(['auth', 'verified'])
    ->name('dashboard');

Route::view('profile', 'profile')
    ->middleware(['auth'])
    ->name('profile');

require __DIR__.'/auth.php';
