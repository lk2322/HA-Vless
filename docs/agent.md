# External Connectivity Check Agent

The Xray External Connectivity Check Agent is a component added to each Xray server that checks the server's ability to connect to external sites like Google, Cloudflare, and GitHub. This helps ensure that HAProxy only routes traffic to Xray servers that have proper external connectivity.

## How It Works

1. The agent runs as a daemon on each Xray server
2. HAProxy sends agent-check requests to the agent
3. When a check is received, the agent attempts to connect to multiple external sites
4. If enough connections succeed, the agent reports "up" to HAProxy
5. If too many connections fail, the agent reports "down" to HAProxy
6. HAProxy automatically routes traffic only to "up" servers

## Configuration Options

In your `group_vars/all.yml` file, you can configure the following agent settings:

```yaml
# Xray Agent Configuration
xray_agent_enabled: true                # Set to false to disable agent-based health checks
xray_agent_port: 8192                   # Port for agent health checks
xray_agent_timeout: 5                   # Timeout for external connectivity checks (seconds)
xray_agent_success_threshold: 3         # Number of successful checks needed to mark server as up
xray_agent_test_sites: "https://www.google.com,https://www.cloudflare.com,https://www.github.com"  # Sites to test connectivity
```

## Logs

Agent logs are written to `/var/log/xray_agent_check.log` on each Xray server.

## Manual Testing

To test the agent directly, you can use telnet on the agent port:

```bash
telnet xray-server-ip 8192
```

The agent will return:
- `0` if the server has good connectivity
- `1` if the server has connectivity issues

## Troubleshooting

1. Check if the agent service is running:
   ```bash
   systemctl status xray-agent
   ```

2. View the agent logs:
   ```bash
   tail -f /var/log/xray_agent_check.log
   ```

3. Test connectivity to the test sites manually:
   ```bash
   curl -v https://www.google.com
   curl -v https://www.cloudflare.com
   ```
