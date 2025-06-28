# Build stage
FROM node:20.12.2-alpine AS build
WORKDIR /ui
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM nginx:alpine
COPY --from=build /ui/dist /usr/share/nginx/html
EXPOSE 3000