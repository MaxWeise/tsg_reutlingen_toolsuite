# Dockerfile for the ReactJS Frontend
FROM node:22-alpine AS build

WORKDIR /app

COPY package*.json ./
RUN npm ci

COPY . .
RUN npm run build

FROM nginx:stable-alpine

COPY --from=build /app/dist /usr/share/nginx/html

# Docker-Run: Startet einen Container im Hintergrund, verbindet Port 8080 auf dem Host mit Port 80 im Container,
# und benennt den Container "frontend-container"
# docker run -d -p 8080:80 --name frontend-container frontend
EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
