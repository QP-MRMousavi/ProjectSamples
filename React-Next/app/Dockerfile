# Use official Node.js image as the base image
FROM node:20.9.0

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
# RUN npm install -g prisma
RUN npm install

# Copy the remaining Next.js project files
COPY . .

# RUN prisma generate

# Expose port
EXPOSE 90

# Command to run the Next.js application
CMD ["npm", "run", "dev"]
