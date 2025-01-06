<?php

namespace App\Models;

use Illuminate\Database\Eloquent\Model;
use Illuminate\Database\Eloquent\Relations\HasMany;

/**
 * @method static where(string $string, string $string1, mixed $getAttribute)
 */
class PackageModel extends Model
{
    const TABLE = 'packages';

    protected $table = self::TABLE;

    protected $fillable = [
        'name',
        'description',
        'original_price',
        'discounted_price',
        'is_active',
        'course_id'
    ];

    public function discountAsPercentage(): string {
        $discount_rate = (
            ($this->getAttribute('original_price') - $this->getAttribute('discounted_price'))
            * 100
            / $this->getAttribute('original_price')
        );
        return number_format($discount_rate, 2) . ' %';
    }

    public function packageIncludes(): HasMany
    {
        return $this->hasMany(PackageIncludeModel::class, 'package_id', 'id');
    }
}
