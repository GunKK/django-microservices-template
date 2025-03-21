FROM node:20.18

# Set working directory
ENV APP_HOME=/usr/src/service
RUN mkdir $APP_HOME

# set work directory
WORKDIR /usr/src/service

RUN apt-get update && apt-get install -y \
    build-essential \
    default-libmysqlclient-dev \
    libpq-dev \
    vim \
    tzdata \
    pkg-config \
    netcat-traditional && \
    rm -rf /var/lib/apt/lists/*

# Install PM2 globally
RUN npm install --global pm2

# Credential for real time monitoring PM2 Plus
ENV PM2_PUBLIC_KEY xxxxx
ENV PM2_SECRET_KEY xxxxx

# Copy all files
COPY ./ $APP_HOME

# Install dependencies
RUN yarn install

# Build app
#RUN npm run build

# Expose the listening port
EXPOSE 9000
EXPOSE 50051

# Launch app with PM2
# CMD [ "pm2-runtime", "start", "npm", "--", "start" ]
