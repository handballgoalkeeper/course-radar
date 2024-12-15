<?php

use App\Models\CourseModel;
use App\Models\CourseProviderModel;
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table(table: CourseModel::TABLE, callback: function (Blueprint $table) {
            $table->unsignedBigInteger(column: 'course_provider_id')->after('id');
            $table->foreign(columns: 'course_provider_id')->references('id')->on(CourseProviderModel::TABLE);
        });
    }

    public function down(): void
    {
        Schema::table(table: CourseModel::TABLE, callback: function (Blueprint $table) {
            $table->dropForeign('');
            $table->dropColumn(columns: 'course_provider_id');
        });
    }
};
