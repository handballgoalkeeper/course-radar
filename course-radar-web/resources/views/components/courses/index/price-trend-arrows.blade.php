@php use App\Enums\CoursePriceTrendNotations; @endphp

@props([
    'priceTrend' => CoursePriceTrendNotations::STABLE->value
])

<div class="text-center position-relative mt-4">
    <span class="course-trend-label">
        Price trend
    </span>
    <div class="border border-dark rounded p-2 px-3">
        @if($priceTrend === CoursePriceTrendNotations::STABLE->value)
            <span class="fw-bold fs-2 p-0 m-0">-</span>
        @endif
        @if($priceTrend === CoursePriceTrendNotations::RISING->value)
            <x-icons.arrow-up-right class="text-danger"/>
        @endif
        @if($priceTrend === CoursePriceTrendNotations::FALLING->value)
            <x-icons.arrow-down-right class="text-success"/>
        @endif
    </div>
</div>
