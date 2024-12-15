<?php

use App\Models\PackageIncludeModel;
use App\Models\PackageModel;
use Illuminate\Database\Migrations\Migration;
use Illuminate\Database\Schema\Blueprint;
use Illuminate\Support\Facades\Schema;

return new class extends Migration
{
    public function up(): void
    {
        Schema::create(table: PackageIncludeModel::TABLE, callback: function (Blueprint $table) {
            $table->id();
            $table->unsignedBigInteger(column: 'package_id');
            $table->text(column: 'text');
            $table->boolean(column: 'is_active')->default(value: true);
            $table->timestamp(column: 'created_at')->useCurrent();

            $table->foreign(columns: 'package_id')->references(columns: 'id')->on(table: PackageModel::TABLE);
        });
    }

    public function down(): void
    {
        Schema::dropIfExists(table: PackageIncludeModel::TABLE);
    }
};
