<?php

namespace App\Livewire\Courses\Index;

use App\Models\CourseModel;
use Illuminate\View\View;
use Livewire\Attributes\Title;
use Livewire\Component;

#[Title('Courses')]
class Page extends Component
{
    public function render(): View
    {
        $courses = CourseModel::all();
        return view(view: 'livewire.courses.index.page', data: [
            'courses' => $courses
        ]);
    }
}
