<?php

namespace App\Configs;

class MainNavigationConfig
{
    public static function getMainNavigation(): array {
        return [
            'Home' => [
                'routeName' => 'home.index',
                'icon' => 'bi-house',
                'permissionNeeded' => null
            ],
            'Courses' => [
                'routeName' => 'courses.index',
                'icon' => 'bi-book',
                'permissionNeeded' => null
            ],
            'Course providers' => [
                'routeName' => 'providers.index',
                'icon' => 'bi-buildings',
                'permissionNeeded' => null
            ],
        ];
    }
}
