<?php

namespace App\Repositories;

use App\Exceptions\NoEntriesFound;
use App\Models\CourseModel;
use Illuminate\Contracts\Queue\EntityNotFoundException;
use Illuminate\Pagination\LengthAwarePaginator;
use PhpOption\None;

class CourseRepository
{
    /**
     * @throws NoEntriesFound
     */
    public function findAllPaginated(int $perPage, string $searchQuery = null): LengthAwarePaginator
    {
        if (is_null($searchQuery)) {
            $courses = CourseModel::paginate(perPage: $perPage);

            if ($courses->isEmpty()) {
                throw new NoEntriesFound(entityName: "Course");
            }

            return $courses;
        }

        $courses = CourseModel::where('title', 'LIKE', "%". $searchQuery ."%")
            ->orWhere('description', 'LIKE', "%". $searchQuery ."%")
            ->paginate(perPage: $perPage);

        if ($courses->isEmpty()) {
            throw new NoEntriesFound(entityName: "Course");
        }

        return $courses;
    }
}
