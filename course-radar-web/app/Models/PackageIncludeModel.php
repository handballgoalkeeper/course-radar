<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;

class PackageIncludeModel extends Model
{
    const TABLE = 'package_includes';

    protected $table = self::TABLE;

    public $timestamps = false;

    protected $fillable = [
        'text',
        'package_id',
    ];
}
