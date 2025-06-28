# Build stage
FROM node:20.12.2-alpine AS build
WORKDIR /ui
COPY package.json package-lock.json ./
RUN npm ci
COPY . .
RUN npm run build    Vite -> /ui/dist

# Runtime stage
FROM nginx:alpine
# Pick whichever build folder exists. If "build" is missing we'll use "dist".
# Comment out the one you *don't* need.
# For Create‑React‑App:
# COPY --from=build /ui/build /usr/share/nginx/html
# For Vite / other tools:
COPY --from=build /ui/dist /usr/share/nginx/html
EXPOSE 3000
CMD ["nginx", "-g", "daemon off;"]