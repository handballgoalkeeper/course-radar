<?php

namespace App\Livewire\Courses\Permalink;

use App\Models\CourseModel;
use Illuminate\View\View;
use Livewire\Component;

class Page extends Component
{
    private CourseModel $course;

    public function mount(CourseModel $course): void
    {
        $this->course = $course;
    }
    public function render(): View
    {
        return view('livewire.courses.permalink.page', [
            'course' => $this->course,
        ]);
    }
}
