<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class CourseProviderModel extends Model
{
    const TABLE = 'course_providers';

    protected $table = self::TABLE;

    protected $fillable = [
        'name',
        'web_site_url',
        'created_at',
        'updated_at'
    ];
}
