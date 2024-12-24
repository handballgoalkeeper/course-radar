<?php

namespace App\Providers;

use App\Repositories\CourseRepository;
use App\Services\CourseService;
use Illuminate\Support\ServiceProvider;

class AppServiceProvider extends ServiceProvider
{
    public function register(): void
    {
        $this->app->singleton(CourseRepository::class, function ($app) {
            return new CourseRepository();
        });

        $this->app->singleton(CourseService::class, function ($app) {
            return new CourseService(
                courseRepository: $app->make(CourseRepository::class)
            );
        });
    }

    public function boot(): void
    {
        //
    }
}
