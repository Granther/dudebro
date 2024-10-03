# Deployment Server
- Deploys, deletes, configures, restarts, ... deployments
- Does so when signaled from web server
- Can run without web server, just handles requests

### Data
- Has its own database of userid and containerid
- Keeps other container data such as deployment config and volume
- Will have external volume for database

### Signals
- Config, for instance, gets sent the new config, userid, containerid, Configures and redeploys

### Load Balancing
- Does the job of adding and removing firewall, dns, proxy machine... entries

### Status
- Returns the container status when asked

### Dockerfile
- Run server on dockerfile boot
- I dont think this will support concurency, only one of these should run at once

## In Depth

### To Start
- Gets most env data
- Must connect to cluster
- Verify connection to DB and nginx load bal

### Signals
- Create, deployment config, game config, subdomain (if applicable), userid -> userid, containerid, status tuple (cont status, custom dudestatus) 

### Ports
- Have a config that describes the port config (ie n, n+400)