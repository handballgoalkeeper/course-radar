<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class PackageModel extends Model
{
    const TABLE = 'packages';

    protected $table = self::TABLE;

    protected $fillable = [
        'name',
        'description',
        'original_price',
        'discount_price',
        'is_active',
        'course_id'
    ];
}
