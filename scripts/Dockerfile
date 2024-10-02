# Base image
FROM ubuntu:latest

# Install Nginx
RUN apt-get update && apt-get install -y nginx

# Expose the default Nginx port (80)
EXPOSE 80

# Start Nginx service
CMD ["nginx", "-g", "daemon off;"]
