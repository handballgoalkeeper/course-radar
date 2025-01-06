<div class="container mt-3">
    <div class="container mb-4">
        <div class="row justify-content-center">
            <div class="col-md-6">
                <div class="search-container">
                    <input
                        wire:model.live.debounce.250ms="search"
                        type="search"
                        class="form-control search-input"
                        placeholder="Search..."
                    >
                </div>
            </div>
        </div>
    </div>
    @if(!is_null($courses))
        <div class="row row-cols-lg-4 row-cols-md-2 row-cols-sm-1 row-cols-md-2 g-4">
            @foreach($courses as $course)
                <div
                    class="col">
                    <section>
                        <div class="card v-2 mt-2 mb-4 rounded-bottom  border border-dark-subtle">
                            <div class="card-body d-flex flex-column">
                                <div class="text-center">
                                    <small>{{ $course->courseProvider->name }}</small>
                                    <h4 class="card-title font-weight-bolder">
                                        {{ $course->title }}
                                    </h4>
                                    <x-courses.index.price-trend-arrows />
                                </div>
                                <hr>
                                <section>
                                    <p>{{ $course->description }}</p>
                                </section>
                                <div class="text-center h-100">
                                    <a
                                        wire:navigate class="btn btn-primary w-100"
                                        href="{{ route('courses.permalink', [ 'course' => $course->id ]) }}"
                                    >
                                        More details
                                    </a>
                                </div>
                            </div>
                        </div>
                    </section>
                </div>
            @endforeach
        </div>
        <div>
            @if(!is_null($courses))
                {{ $courses->links() }}
            @endif
        </div>
    @endif
</div>
