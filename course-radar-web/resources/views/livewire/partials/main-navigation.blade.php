<nav class="navbar navbar-expand-lg navbar-light bg-light px-5">
        <a wire:navigate class="navbar-brand" href="/">
            <x-icons.radar-line />
            Course Radar
        </a>
        <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarSupportedContent" aria-controls="navbarSupportedContent" aria-expanded="false" aria-label="Toggle navigation">
            <span class="navbar-toggler-icon"></span>
        </button>

        <div class="collapse navbar-collapse" id="navbarSupportedContent">
            <ul class="navbar-nav w-100">
                @foreach($navItems as $routeName => $routeMeta)
                    <li class="nav-item">
                        <a
                            wire:navigate
                            @class([
                                'nav-link',
                                'active' => Route::is($routeMeta['routeName'])
                            ])
                            href="{{ route($routeMeta['routeName']) }}">
                            {{ $routeName }}
                        </a>
                    </li>
                @endforeach
            </ul>
        </div>
</nav>
