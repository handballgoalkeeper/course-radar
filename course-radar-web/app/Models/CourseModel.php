<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasOne;

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

    public function courseProvider(): HasOne
    {
        return $this->hasOne(CourseProviderModel::class, 'id', 'course_provider_id');
    }
}
