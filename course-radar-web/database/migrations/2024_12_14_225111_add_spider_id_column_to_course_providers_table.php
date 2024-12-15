<?php

use App\Models\CourseProviderModel;
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::table(table: CourseProviderModel::TABLE, callback: function (Blueprint $table) {
            $table->unsignedBigInteger(column: 'spider_id')->after('web_site_url');
        });
    }

    public function down(): void
    {
        Schema::table(table: CourseProviderModel::TABLE, callback: function (Blueprint $table) {
            $table->dropColumn('spider_id');
        });
    }
};
