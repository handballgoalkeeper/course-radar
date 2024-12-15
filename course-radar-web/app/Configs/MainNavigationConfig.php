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
            'Course provider' => [
                'routeName' => 'providers.index',
                'icon' => 'bi-buildings',
                'permissionNeeded' => null
            ],
        ];
    }
}
