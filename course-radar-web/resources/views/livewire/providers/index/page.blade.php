<div class="container mt-2">
    <div
        x-data="{
            newTab(url) {
                window.open(url, '_blank');
            }
        }"
        class="row row-cols-lg-4 row-cols-md-2 row-cols-sm-1 row-cols-md-2 g-4">
        @foreach($providers as $provider)
            <div
                class="col">
                <div class="container">
                    <section class="mx-auto my-5" style="max-width: 23rem;">
                        <div class="card booking-card v-2 mt-2 mb-4 rounded-bottom  border border-dark-subtle">
                            <div class="bg-image">
                                <img class="w-100 rounded-top" src="https://placehold.co/600x400">
                            </div>
                            <div class="card-body">
                                <h4
                                    @click="newTab('{{ $provider->web_site_url }}')"
                                    class="text-center card-title font-weight-bold"
                                >
                                        {{ $provider->name }}
                                </h4>
                            </div>
                        </div>
                    </section>
                </div>
            </div>
        @endforeach
    </div>
</div>
