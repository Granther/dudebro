# Use the correct base image
FROM debian:slim-dude

# Set the working directory
WORKDIR /home/mc-server/

# Copy the start.sh script into the container
COPY start.sh /home/mc-server/start.sh

# Make the script executable
RUN chmod +x /home/mc-server/start.sh

# Set the default command to execute the script
CMD ["./start.sh"]
