FROM node:20.11-slim

WORKDIR /app

# Install dependencies
COPY package*.json ./
RUN npm ci

# Copy source (changed from 'hospital-ids' to '.')
COPY . .

# Build application
RUN npm run build

# Drop root privileges
RUN chown -R node:node .
USER node

EXPOSE 3000

CMD ["npm", "start"]