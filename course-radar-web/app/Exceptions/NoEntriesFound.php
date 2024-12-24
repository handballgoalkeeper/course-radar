<?php

namespace App\Exceptions;

use Exception;

class NoEntriesFound extends Exception
{
    public function __construct(string $entityName)
    {
        parent::__construct(message: 'No entries available for this entity "' . $entityName . '".');
    }
}
