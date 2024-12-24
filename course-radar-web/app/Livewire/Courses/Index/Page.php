<?php

namespace App\Livewire\Courses\Index;

use App\Enums\ErrorMessage;
use App\Exceptions\NoEntriesFound;
use App\Services\CourseService;
use Exception;
use Illuminate\View\View;
use Livewire\Attributes\Title;
use Livewire\Attributes\Url;
use Livewire\Component;
use Livewire\WithPagination;

#[Title('Courses')]
class Page extends Component
{
    use withPagination;
    #[Url]
    public string $search = '';

    public function render(CourseService $courseService): View
    {
        try {
            $courses = $courseService->findAllPaginated(search: $this->search);
        }
        catch (NoEntriesFound $exception) {
            return view(view: 'livewire.courses.index.page', data: [
                'courses' => null,
                'error' => $exception->getMessage()
            ]);
        }
        catch (Exception $e) {
            return view(view: 'livewire.courses.index.page', data: [
                'courses' => null,
                'error' => ErrorMessage::UNHANDLED_EXCEPTION
            ]);
        }

        return view(view: 'livewire.courses.index.page', data: [
            'courses' => $courses
        ]);
    }

    public function updatedSearch(): void
    {
        $this->resetPage();
    }
}
