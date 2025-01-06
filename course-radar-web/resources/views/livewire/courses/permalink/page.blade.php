<div class="container border border-dark-subtle rounded mt-2">
    <div class="row">
        <div class="col-12 text-center mt-2">
            <h3>{{ $course->title }}</h3>
        </div>
    </div>
    <hr>
    <div class="row text-center">
        <div class="col-12">
            <p>{{ $course->description }}</p>
        </div>
    </div>
    <div class="container shadow p-4 mb-4 bg-body rounded">
        <div class="row table-responsive">
            <table class="table table-striped">
                <caption>Course packages pricing list</caption>
                <thead>
                    <tr>
                        <th scope="col">#</th>
                        <th scope="col">Name</th>
                        <th scope="col">Description</th>
                        <th scope="col">Original price</th>
                        <th scope="col">Discount</th>
                        <th scope="col">Discounted price</th>
                        <th scope="col">Actions</th>
                    </tr>
                </thead>
                <tbody>
                @foreach($course->packages as $package)
                    <tr>
                        <th scope="row">{{ $loop->iteration }}</th>
                        <td>{{ $package->name }}</td>
                        <td>{{ $package->description }}</td>
                        <td>{{ $package->original_price }}</td>
                        <td class="fw-bolder">{{ $package->discountAsPercentage() }}</td>
                        <td>{{ $package->discounted_price }}</td>
                        <td>
                            @if(!$package->packageIncludes->isEmpty())
                                <button class="btn btn-primary">Details</button>
                            @endif
                        </td>
                    </tr>
                @endforeach
                </tbody>
            </table>
        </div>
    </div>
</div>
