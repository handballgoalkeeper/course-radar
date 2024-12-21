<?php

namespace App\Livewire\Home\Index;

use Illuminate\View\View;
use Livewire\Attributes\Title;
use Livewire\Component;

#[Title('Home')]

class Page extends Component
{
    public function render(): View
    {
        return view('livewire.home.index.page');
    }
}
