<?php

namespace App\Services;

use App\Exceptions\NoEntriesFound;
use App\Repositories\CourseRepository;
use Illuminate\Pagination\LengthAwarePaginator;

class CourseService
{
    public function __construct(
        protected CourseRepository $courseRepository
    )
    {
    }

    /**
     * @throws NoEntriesFound
     */
    public function findAllPaginated(string $search, int $perPage = 12): LengthAwarePaginator
    {
        return $this->courseRepository->findAllPaginated(perPage: $perPage, searchQuery: $search);
    }

}
