# Use the correct base image
FROM debian:trixie-slim

RUN useradd -ms /bin/bash dude
USER dude

# Set the working directory
WORKDIR /minecraft

# Set the default command to execute the script
CMD ["./start.sh"]
