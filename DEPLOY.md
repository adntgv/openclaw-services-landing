# Deployment Instructions for Coolify

## Quick Deploy

1. **Open Coolify Dashboard**
   - Navigate to http://localhost:3000 (or your Coolify URL)
   - Login with your credentials

2. **Create New Application**
   - Click "+ New" → "Application"
   - Select your server (usually "localhost")
   - Choose "Docker" as deployment method

3. **Configure Application**
   ```
   Name: openclaw-services-landing
   Source: GitHub
   Repository: adntgv/openclaw-services-landing
   Branch: master
   Build Pack: Dockerfile
   Port: 80
   ```

4. **Set Domain**
   ```
   FQDN: openclaw.adntgv.com
   ```
   
   Make sure to add DNS A record:
   ```
   Type: A
   Name: openclaw
   Value: YOUR_SERVER_IP
   ```

5. **Deploy**
   - Click "Deploy" button
   - Wait for build to complete (~2-3 minutes)
   - Site will be live at https://openclaw.adntgv.com

## Alternative: Manual Docker Deploy

If Coolify is not available, deploy manually:

```bash
cd ~/workspace/openclaw-services-landing

# Build image
docker build -t openclaw-services .

# Run container
docker run -d \
  --name openclaw-services \
  --network coolify \
  -p 8080:80 \
  --restart unless-stopped \
  openclaw-services

# Add Traefik labels for HTTPS
docker run -d \
  --name openclaw-services \
  --network coolify \
  --label "traefik.enable=true" \
  --label "traefik.http.routers.openclaw.rule=Host(\`openclaw.adntgv.com\`)" \
  --label "traefik.http.routers.openclaw.entrypoints=websecure" \
  --label "traefik.http.routers.openclaw.tls.certresolver=letsencrypt" \
  --label "traefik.http.services.openclaw.loadbalancer.server.port=80" \
  --restart unless-stopped \
  openclaw-services
```

## Verify Deployment

1. Check if site loads: https://openclaw.adntgv.com
2. Test mobile responsiveness
3. Verify contact form works
4. Check all images load
5. Test navigation links

## Troubleshooting

### Container won't start
```bash
docker logs openclaw-services
```

### Domain not resolving
1. Check DNS propagation: `dig openclaw.adntgv.com`
2. Verify Cloudflare DNS settings
3. Wait 5-10 minutes for DNS propagation

### SSL/HTTPS issues
1. Check Traefik logs: `docker logs traefik`
2. Verify domain is proxied through Cloudflare (orange cloud)
3. Ensure Cloudflare SSL mode is "Full (strict)"

## Updates

To deploy updates:

```bash
cd ~/workspace/openclaw-services-landing
git pull
docker build -t openclaw-services .
docker stop openclaw-services
docker rm openclaw-services
# Run docker command from above
```

Or via Coolify: just push to GitHub and it auto-deploys.