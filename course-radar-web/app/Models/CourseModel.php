<?php

namespace App\Models;

use App\Enums\CoursePriceTrendNotations;
use Illuminate\Database\Eloquent\Collection;
use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;
use Illuminate\Database\Eloquent\Relations\HasOne;
use Illuminate\Support\Facades\DB;

/**
 * @method static paginate(int $perPage)
 */
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

    public function packages(): HasMany
    {
        return $this->hasMany(PackageModel::class, 'course_id', 'id');
    }
}
