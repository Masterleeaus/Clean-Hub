<?php

declare(strict_types=1);

namespace App\Support\TitanZero;

final readonly class TitanZeroFeatureFlags
{
    private const WORKCORE_PROVIDER = 'App\\Domains\\WorkCore\\WorkCoreServiceProvider';
    private const CHATBOT_PROVIDER = 'App\\Extensions\\Chatbot\\System\\ChatbotServiceProvider';
    private const EXTENSION_PROVIDER = 'App\\Providers\\ExtensionServiceProvider';

    private function __construct(
        private bool $workcoreEnabled,
        private bool $chatbotEnabled,
        private bool $interactionEngineEnabled,
        private bool $extensionDiscoveryEnabled,
    ) {
    }

    /** @param array<string, mixed> $config */
    public static function fromArray(array $config): self
    {
        return new self(
            workcoreEnabled: (bool) ($config['workcore_enabled'] ?? true),
            chatbotEnabled: (bool) ($config['chatbot_enabled'] ?? false),
            interactionEngineEnabled: (bool) ($config['interaction_engine_enabled'] ?? false),
            extensionDiscoveryEnabled: (bool) ($config['extension_discovery_enabled'] ?? false),
        );
    }

    public function workCoreEnabled(): bool
    {
        return $this->workcoreEnabled;
    }

    public function chatbotEnabled(): bool
    {
        return $this->chatbotEnabled;
    }

    public function interactionEngineEnabled(): bool
    {
        return $this->interactionEngineEnabled;
    }

    public function extensionDiscoveryEnabled(): bool
    {
        return $this->extensionDiscoveryEnabled;
    }

    /** @return list<class-string<\Illuminate\Support\ServiceProvider>> */
    public function coreProviderClassNames(): array
    {
        $providers = [];

        if ($this->workcoreEnabled) {
            $providers[] = self::WORKCORE_PROVIDER;
        }

        if ($this->chatbotEnabled) {
            $providers[] = self::CHATBOT_PROVIDER;
        }

        if ($this->extensionDiscoveryEnabled) {
            $providers[] = self::EXTENSION_PROVIDER;
        }

        return $providers;
    }
}
