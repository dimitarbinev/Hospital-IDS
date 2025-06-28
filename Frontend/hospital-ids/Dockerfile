# Build stage
FROM node:20.12.2-alpine AS build
WORKDIR /ui
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build

# Runtime stage
FROM nginx:alpine
# React (create‑react‑app) outputs to /ui/build ; Vite outputs to /ui/dist.
# If your build folder is `dist`, swap the line below accordingly.
COPY --from=build /ui/build /usr/share/nginx/html
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]
```Dockerfile
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