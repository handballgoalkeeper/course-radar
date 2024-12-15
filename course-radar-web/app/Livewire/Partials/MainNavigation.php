<?php

namespace App\Livewire\Partials;

use App\Configs\MainNavigationConfig;
use Illuminate\View\View;
use Livewire\Component;

class MainNavigation extends Component
{
    public function render(): View
    {
        return view(view: 'livewire.partials.main-navigation', data: [
            'navItems' => MainNavigationConfig::getMainNavigation()
        ]);
    }
}
