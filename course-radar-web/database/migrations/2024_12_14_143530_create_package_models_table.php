<?php

use App\Models\CourseModel;
use App\Models\PackageModel;
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create(table: PackageModel::TABLE, callback: function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger(column: 'course_id');
            $table->string(column: 'name', length: 255);
            $table->text(column: 'description')->nullable();
            $table->float(column: 'original_price');
            $table->float(column: 'discounted_price');
            $table->boolean(column: 'is_active')->default(value: true);
            $table->timestamps();

            $table->foreign(columns: 'course_id')->references(columns: 'id')->on(table: CourseModel::TABLE);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists(table: PackageModel::TABLE);
    }
};
