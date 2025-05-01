# Contributing to HA-vless

Thank you for considering contributing to HA-vless! This document provides some guidelines to help you get started.

## How to Contribute

1. Fork the repository
2. Create a feature branch: `git checkout -b my-new-feature`
3. Make your changes
4. Commit your changes: `git commit -am 'Add some feature'`
5. Push to the branch: `git push origin my-new-feature`
6. Submit a pull request

## Development Guidelines

- Follow Ansible best practices
- Use the same style and formatting as the rest of the codebase
- Add comments to explain complex sections
- Update documentation for any user-facing changes

## Testing

Before submitting a pull request, please test your changes on:
- At least one HAProxy server
- At least one Xray server (main or backup)

## Adding Support for New DNS Providers

To add support for a new DNS provider for certificate issuance:

1. Update the `templates/dns_env.j2` file with the environment variables needed for the DNS provider
2. Update documentation in README.md
3. Test with the new DNS provider

## License

By contributing to HA-vless, you agree that your contributions will be licensed under the project's MIT license.