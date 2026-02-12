FROM nginx:latest

# Copy nginx base config
COPY nginx.conf /etc/nginx/nginx.conf

# Copy site configs
COPY conf.d /etc/nginx/conf.d

# Copy certificates
COPY certs /etc/nginx/certs