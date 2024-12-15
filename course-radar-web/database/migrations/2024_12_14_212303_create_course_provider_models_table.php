<?php

use App\Models\CourseProviderModel;
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create(table: CourseProviderModel::TABLE, callback: function (Blueprint $table) {
            $table->id();
            $table->string(column: "name");
            $table->string(column: "web_site_url");
            $table->timestamps();
        });
    }

    public function down(): void
    {
        Schema::dropIfExists(table: CourseProviderModel::TABLE);
    }
};
