## Dude Bro Hosting
- Hosting simple servers, vanilla survival with minimal customization
- Cheap, maybe even pay by week
- Would start out free as test

### Backend
- Python Docker SDK backend
- Give people own subdomain, use reverse proxy to route traffic based on subdom
- The subdomain will just resolve to my ip
- When creating a server, nginx will add the user's unique name as a subdomain to the routes
- Nginx will use the ip associated with the container for this
- The container will be created with a label for the user's id or something
- Would like to keep the backend pretty simple

### Features
- Shutdown, start, reboot
- Whitelist, Blacklist
- 

### Deployment API
- Create Server
- Delete server
- Store user data for retrieval
- Star, Stop, Restart
- Configure, ie. name, access FS
- Make sure resources are avilable

### Other
- UserID will be unique and generated when user is created 

### Create server
- Get userid, subdomain
- Deploy and start complete server with labels
- Get IP
- Set config in Nginx with IP and subdom
- Give user subdom

### Front End
- Seems like most of the backend is written
- Simple user creation
- 1 container per user (check_num_own)
- Interaction with backend

### Interaction with MC server
- Edit server.prop but in special mode. ie, cant edit port

### To Do
- Backend interaction to customize serer props
- What else needs to be edited? 
- Op/Deop players
- View logs
- Download and upload world

### MC Dudebro Interactor Server
- Runs on the container alongside the MC server
- Mother server GETS and POSTs changes 

### Changes that can be made
- I'm just gonna assume that I can change files while the server is running without issues

### To Do
- Asyn restart since it holds up
- If a create fails, clean up what its already done
- Check fo DNS
- Dont create dir