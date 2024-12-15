<?php

use App\Models\CourseModel;
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create(table: CourseModel::TABLE, callback: function (Blueprint $table) {
            $table->id();
            $table->string(column: 'title', length: 255);
            $table->text(column: 'description')->nullable();
            $table->boolean(column: 'is_active')->default(value: true);
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists(table: CourseModel::TABLE);
    }
};
