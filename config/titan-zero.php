<?php

declare(strict_types=1);

$enabledExtensions = array_values(array_filter(array_map(
    static fn (string $identifier): string => trim($identifier),
    explode(',', (string) env('TITAN_ZERO_EXTENSIONS_ENABLED', '')),
)));

return [
    'workcore_enabled' => env('TITAN_ZERO_WORKCORE_ENABLED', true),
    'chatbot_enabled' => env('TITAN_ZERO_CHATBOT_ENABLED', false),
    'interaction_engine_enabled' => env('TITAN_ZERO_INTERACTION_ENGINE_ENABLED', false),
    'extension_discovery_enabled' => env('TITAN_ZERO_EXTENSION_DISCOVERY_ENABLED', false),
    'extensions' => [
        'enabled' => $enabledExtensions,
    ],
];
