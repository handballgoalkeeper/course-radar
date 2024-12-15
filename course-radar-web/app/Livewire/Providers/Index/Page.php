<?php

namespace App\Livewire\Providers\Index;

use App\Models\CourseProviderModel;
use Illuminate\View\View;
use Livewire\Component;

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
