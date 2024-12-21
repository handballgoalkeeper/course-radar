<?php

namespace App\Livewire\Providers\Index;

use App\Models\CourseProviderModel;
use Illuminate\View\View;
use Livewire\Attributes\Title;
use Livewire\Component;

#[Title('Course providers')]
class Page extends Component
{
    public function render(): View
    {
        $providers = CourseProviderModel::all();
        return view('livewire.providers.index.page', [
            'providers' => $providers
        ]);
    }
}
