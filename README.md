# HA-Vless: High-Availability Xray Proxy with HAProxy

This Ansible playbook sets up a high-availability Xray proxy system using HAProxy for load balancing. The setup includes:

- HAProxy as a TCP proxy for load balancing
- Multiple Xray servers (main and backup) with automatic failover
- TLS certificate management using acme.sh with DNS challenge
- Self-signed certificate fallback when ACME challenges fail
- Docker Compose for all service deployments
- Easy management of multiple clients
- Support for both VLESS protocol and HTTP proxy
- External connectivity check agent for reliable failover

## Prerequisites

- Ansible 2.9+
- Target servers with Ubuntu/Debian-based OS
- DNS provider API access for certificate issuance

## Quick Start

1. Clone this repository:
   ```bash
   git clone https://github.com/lk2322/HA-Vless.git
   cd HA-Vless
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

## Generate Client Connection Information

To generate connection URLs, configuration files, and QR codes for all clients:

```bash
# Using the playbook directly
ansible-playbook -i inventory.yml show-client-urls.yml

# Or using the Makefile
make show-urls
```

This will create:

1. **Individual client configuration files** in the `client_configs/` directory
   - One file per client named after their email address
   - Each file contains the client's UUID and formatted VLESS URL
   - HTTP proxy information is included if enabled

2. **Consolidated configuration file** at `client_configs/all_clients.txt`
   - Contains connection information for all clients in one file
   - Includes HTTP proxy details if enabled

3. **QR codes** in the `client_qrcodes/` directory
   - One QR code image per client named after their email address
   - Can be scanned directly with mobile apps like v2rayNG or Shadowrocket
   - Requires `qrencode` to be installed on your system

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

## Monitoring

HA-vless includes a comprehensive monitoring solution using Prometheus and Grafana. This allows you to monitor the health and performance of your HAProxy load balancer, Xray servers, and system metrics.

### Features

- **Prometheus** for metrics collection and storage
- **Grafana** for metrics visualization with pre-configured dashboards
- **Node Exporter** for system metrics (CPU, memory, disk, network)
- **HAProxy Exporter** for detailed HAProxy statistics

### Dashboards

The monitoring setup includes three pre-configured Grafana dashboards:

1. **HAProxy Overview**: Monitor connection counts, backend status, and proxy performance
2. **System Metrics**: Track CPU, memory, disk usage, and network traffic across all servers
3. **Xray Metrics**: Visualize Xray active connections and traffic throughput

### Configuration

To enable or customize the monitoring stack:

1. In `group_vars/all.yml`, configure the monitoring settings:
   ```yaml
   # Monitoring Configuration
   monitoring_enabled: true  # Set to false to disable monitoring
   prometheus_port: 9090     # Prometheus web interface port
   grafana_port: 3000        # Grafana web interface port
   grafana_admin_password: admin  # Change this to a secure password
   haproxy_stats_port: 8404  # HAProxy statistics port
   ```

2. Access the monitoring interfaces:
   - Grafana: `http://<haproxy-server>:3000` (login with admin/your_password)
   - Prometheus: `http://<haproxy-server>:9090`
   - HAProxy Stats: `http://<haproxy-server>:8404/haproxy` (login with admin/admin)

### Security Note

The monitoring endpoints are exposed on their respective ports. For production use, consider:
- Changing default passwords
- Setting up a reverse proxy with authentication
- Using firewall rules to restrict access to trusted IPs

## Documentation

- [Main README](README.md) - This file
- [Agent Documentation](docs/agent.md) - External connectivity check agent details

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