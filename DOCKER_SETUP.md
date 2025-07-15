# Docker Setup for Ultimate POS

This guide explains how to run the Ultimate POS application using Docker.

## Development Setup

1. Make sure you have Docker and Docker Compose installed on your machine.
2. Create a `.env` file based on the `.example.env` template:
   ```bash
   cp .example.env .env
   ```
3. Update the `.env` file with your database credentials and other settings.
4. Build and run the containers:
   ```bash
   docker-compose up --build
   ```
5. Access the application at http://localhost:80

## Production Setup

1. Create a `.env` file for production:
   ```bash
   cp .example.env .env
   ```
2. Update the `.env` file with your production credentials and settings.
3. Build and run the production containers:
   ```bash
   docker-compose -f docker-compose.prod.yml up --build -d
   ```

## SSL Configuration

For SSL/HTTPS configuration:

1. Obtain SSL certificates (e.g., using Let's Encrypt).
2. Create a directory for your SSL certificates:
   ```bash
   mkdir -p nginx/ssl
   ```
3. Place your certificates in the nginx/ssl directory:
   - `fullchain.pem`: Your certificate chain
   - `privkey.pem`: Your private key
4. Uncomment the SSL configuration in `nginx/production.conf` and the volume mount in `docker-compose.prod.yml`.
5. Restart the nginx service:
   ```bash
   docker-compose -f docker-compose.prod.yml restart nginx
   ```
