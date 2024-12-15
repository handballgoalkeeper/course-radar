<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class CourseModel extends Model
{
    const TABLE ='courses';

    protected $table = self::TABLE;

    protected $fillable = [
        'course_provider_id',
        'title',
        'description',
        'is_active'
    ];
}
