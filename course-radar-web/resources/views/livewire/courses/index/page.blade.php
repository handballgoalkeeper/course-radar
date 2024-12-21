<div class="container mt-2">
    <div
        x-data="{
            newTab(url) {
                window.open(url, '_blank');
            }
        }"
        class="row row-cols-lg-4 row-cols-md-2 row-cols-sm-1 row-cols-md-2 g-4">
        @foreach($courses as $course)
            <div
                class="col">
                <section class="" style="max-width: 23rem;">
                    <div class="card course-card v-2 mt-2 mb-4 rounded-bottom  border border-dark-subtle">
                        <div class="bg-image">
                            <img class="w-100 rounded-top" src="https://placehold.co/600x400">
                        </div>
                        <div class="card-body d-flex flex-column">
                            <div class="text-center">
                                <small>{{ $course->courseProvider->name }}</small>
                                <h4 class="card-title font-weight-bolder">
                                    {{ $course->title }}
                                </h4>
                            </div>
                            <hr>
                            <section>
                                <p>{{ $course->description }}</p>
                            </section>
                            <div class="text-center h-100">
                                <a wire:navigate class="btn btn-primary w-100" href="">More details</a>
                            </div>
                        </div>
                    </div>
                </section>
            </div>
        @endforeach
    </div>
</div>
