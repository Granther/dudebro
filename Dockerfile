# Use the correct base image
FROM debian:slim-dude

RUN useradd -ms /bin/bash dude
USER dude

#RUN apt update && apt upgrade -y

# Set the working directory
WORKDIR /minecraft

# Copy the start.sh script into the container
# COPY start.sh /home/mc-server/start.sh

# Set the default command to execute the script
CMD ["./start.sh"]
