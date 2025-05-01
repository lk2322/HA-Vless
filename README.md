# HA-vless: High-Availability Xray Proxy with HAProxy

This Ansible playbook sets up a high-availability Xray proxy system using HAProxy for load balancing. The setup includes:

- HAProxy as a TCP proxy for load balancing
- Multiple Xray servers (main and backup) with automatic failover
- TLS certificate management using acme.sh with DNS challenge
- Self-signed certificate fallback when ACME challenges fail
- Docker Compose for all service deployments
- Easy management of multiple clients
- Support for both VLESS protocol and HTTP proxy

## Prerequisites

- Ansible 2.9+
- Target servers with Ubuntu/Debian-based OS
- DNS provider API access for certificate issuance

## Quick Start

1. Clone this repository:
   ```bash
   git clone https://github.com/lk2322/HA-vless.git
   cd HA-vless
   ```

2. Create your inventory file from the example:
   ```bash
   cp inventory.example.yml inventory.yml
   ```

3. Edit the inventory file with your server details:
   ```bash
   nano inventory.yml
   ```

4. Create and customize your variables file:
   ```bash
   cp group_vars/all.example.yml group_vars/all.yml
   nano group_vars/all.yml
   ```

5. Install required roles and collections:
   ```bash
   ansible-galaxy install -r requirements.yml
   ```

6. Run the playbook:
   ```bash
   ansible-playbook -i inventory.yml site.yml
   ```

## Update Client Configuration

To update only Xray configurations (e.g., add/remove clients):

1. Edit the client list in `group_vars/all.yml`
2. Run the update-only playbook:
   ```bash
   ansible-playbook -i inventory.yml update-xray-config.yml
   ```

## Proxy Features

### VLESS Protocol

The VLESS protocol is enabled by default on port 443 with TLS encryption. This is suitable for clients that support the VLESS protocol, such as:
- Xray-core
- v2rayNG
- Qv2ray
- Shadowrocket

### HTTP Proxy (Optional)

An HTTP proxy is also available for clients that don't support VLESS. This can be enabled or disabled in the configuration.

To configure the HTTP proxy:

1. In `group_vars/all.yml`, ensure the HTTP proxy is enabled:
   ```yaml
   # HTTP Proxy Configuration
   xray_http_enabled: true  # Set to false to disable HTTP proxy
   xray_http_port: 8080     # HTTP proxy port
   xray_http_user: "username"  # Change this to your desired username
   xray_http_pass: "password"  # Change this to a strong password
   ```

2. HAProxy will automatically expose port 8080 (or your configured port) for the HTTP proxy service.

3. Configure your clients to use the HTTP proxy with your server address, port, username, and password.

## Server Architecture

```
                   ┌─────────────┐
                   │    Client   │
                   └──────┬──────┘
                          │
                   ┌──────▼──────┐
                   │   HAProxy   │
                   └──────┬──────┘
                          │
           ┌──────────────┴──────────────┐
           │                             │
    ┌──────▼──────┐             ┌────────▼────────┐
    │ Xray Main 1 │             │ Xray Backup 1   │
    └─────────────┘             └─────────────────┘
           |                             |
    ┌─────────────┐             ┌─────────────────┐
    │ Xray Main 2 │             │ Xray Backup 2   │
    └─────────────┘             └─────────────────┘
            ⋮                           ⋮
```

## Configuration Files

- `inventory.yml` - Server inventory
- `group_vars/all.yml` - Main configuration variables
- `site.yml` - Main playbook for full setup
- `update-xray-config.yml` - Playbook for updating Xray configs only

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.