# Nginx

This guide details the steps for installing, configuring, and securing Nginx, including setting up SSL certificates.

## Installation

To install Nginx on a Debian-based system without any recommended packages, use the following command:

```bash
sudo apt install --no-install-recommends -yqq nginx
```

Enable Nginx to start automatically at system boot:

```bash
sudo systemctl enable nginx
```

## Configuration

### Prerequisites

Before editing the Nginx configuration, ensure that DNS settings are properly configured for both of your domains. You will need one domain for each of the Docker services:

- **Private Tracker Service:** Assign a domain that will be used specifically for accessing the private tracker's web user interface.
- **Public Tracker Service:** Assign a separate domain for the public tracker's web user interface.

These domain names will be used in the Nginx configuration to route traffic to the respective services. Make sure that the DNS records for these domains are pointing to the server where Nginx is installed.

### Installing Certbot for SSL

To install Certbot and its Nginx plugin, which are necessary for acquiring SSL certificates, use the command:

```bash
sudo apt-get install certbot python3-certbot-nginx -y
```

### Configuring Nginx

Edit the Nginx configuration file located at `/etc/nginx/sites-available/default`. Replace placeholder domain names with your actual domain names. Below is a sample configuration:

```nginx
server {
    server_name my_domain_private_tracker_webui.com;
    listen 80 default_server;  # This server will handle all HTTP requests by default

    location / {
        proxy_pass http://localhost:8888;  # Proxy traffic to the private tracker
    }
}

server {
    server_name my_domain_public_tracker_webui.com;
    listen 80;  # Standard server, not the default

    location / {
        proxy_pass http://localhost:8080;  # Proxy traffic to the public tracker
    }
}
```

### Reloading Nginx

Validate and reload Nginx to apply changes:

```bash
sudo nginx -t && sudo nginx -s reload
```

#### Notes:
- Port `8888` corresponds to the `config_qbittorrent_private_trackers` Docker Compose service. Refer to the `QBITTORRENT_PRIVATE_WEBUI_PORT` setting.
- Port `8080` corresponds to the `config_qbittorrent_public_trackers` Docker Compose service. Refer to the `QBITTORRENT_PUBLIC_WEBUI_PORT` setting.

## Securing with SSL

To secure your domains with SSL certificates provided by Let's Encrypt, run the following Certbot commands for each domain:

```bash
sudo certbot --nginx -d my_domain_public_tracker_webui.com
sudo certbot --nginx -d my_domain_private_tracker_webui.com
```

These commands will automatically configure SSL for your specified domains using Certbot and adjust the Nginx configuration accordingly.
