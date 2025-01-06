<?php

namespace App\Enums;

enum CoursePriceTrendNotations: string
{
    case RISING = "rising";
    case FALLING = 'falling';
    case STABLE = 'stable';
}
