# Deploy a Django Project on AWS EC2 using Gunicorn and Nginx  

This guide explains how to deploy a Django application on an AWS EC2 instance using **Gunicorn** as the WSGI server and **Nginx** as the reverse proxy.  

---

## Prerequisites  
- An **AWS EC2 instance** (Ubuntu).  
- Basic knowledge of Django and Linux commands.  
- A Django project repository on GitHub.  

---

## Deployment Steps  

### 1. **Update and Upgrade the Server**  
Run the following commands to ensure the server is up to date:  
```bash  
sudo apt-get update  
sudo apt-get upgrade  
```  

### 2. **Install Python and Create a Virtual Environment**  
Check if Python is installed and set up a virtual environment:  
```bash  
python3 --version  
sudo apt-get install python3-venv  
python3 -m venv env  
source env/bin/activate  
```  

### 3. **Install Django and Whitenoise**  
Inside the virtual environment, install Django and Whitenoise for static file management:  
```bash  
pip install django  
pip install whitenoise  
```  

### 4. **Clone the Django Project**  
Clone your project from GitHub:  
```bash  
git clone https://github.com/harshadakhorgade/demo_project.git  
cd demo_project  
```  

### 5. **Install Gunicorn and Nginx**  
Install Gunicorn for running the application and Nginx as a reverse proxy:  
```bash  
sudo apt-get install -y nginx  
pip install gunicorn  
```  

### 6. **Configure Gunicorn with Supervisor**  
Install Supervisor to manage Gunicorn as a service:  
```bash  
sudo apt-get install supervisor  
cd /etc/supervisor/conf.d/  
sudo touch gunicorn.conf  
sudo nano gunicorn.conf  
```  

Add the following configuration to `gunicorn.conf`:  
```ini  
[program:gunicorn]  
directory=/home/ubuntu/demo_project  
command=/home/ubuntu/env/bin/gunicorn --workers 3 --bind unix:/home/ubuntu/demo_project/app.sock demo_project.wsgi:application  
autostart=true  
autorestart=true  
stderr_logfile=/var/log/gunicorn/gunicorn.err.log  
stdout_logfile=/var/log/gunicorn/gunicorn.out.log  

[group:guni]  
programs:gunicorn  
```  

Save and exit (`Ctrl+O`, `Enter`, `Ctrl+X`).  

Create the Gunicorn log directory:  
```bash  
sudo mkdir /var/log/gunicorn  
```  

Reload and start Supervisor:  
```bash  
sudo supervisorctl reread  
sudo supervisorctl update  
sudo supervisorctl status  
```  



### 7. **Configure Nginx**  
Follow these steps to set up Nginx as the reverse proxy for your Django application:

1. **Navigate to the Nginx Configuration Directory**  
   Use the following commands to locate and verify the Nginx configuration files:  
   ```bash  
   cd ..  
   cd ..  
   ls  
   cd nginx  
   ls  
   ```  

2. **Change the Nginx User (Optional)**  
   If necessary, edit the main Nginx configuration file:  
   ```bash  
   sudo nano /etc/nginx/nginx.conf  
   ```  
   Modify the `user` line to:  
   ```nginx  
   user root;  
   ```  

3. **Set Up Site Configuration**  
   Navigate to the `sites-available` directory:  
   ```bash  
   cd /etc/nginx/sites-available  
   sudo touch Django.conf  
   sudo nano Django.conf  
   ```  

   Add the following content:  
   ```nginx  
   server {  
       listen 80;  
       server_name <your-public-IP>;  

       location / {  
           include proxy_params;  
           proxy_pass http://unix:/home/ubuntu/demo_project/app.sock;  
       }  
   }  
   ```  

4. **Enable the Site and Restart Nginx**  
   Test the Nginx configuration and enable your Django site:  
   ```bash  
   sudo nginx -t  
   sudo ln -s /etc/nginx/sites-available/Django.conf /etc/nginx/sites-enabled  
   sudo service nginx restart  
   ```  

---

### 8. **Access Your Application**  
- Open a browser and visit: `http://<your-public-IP>`  
- Your Django application should now be live!  

---

## Logs and Debugging  
- **Gunicorn logs**:  
  - Standard: `/var/log/gunicorn/gunicorn.out.log`  
  - Error: `/var/log/gunicorn/gunicorn.err.log`  

- **Nginx logs**:  
  - Access: `/var/log/nginx/access.log`  
  - Error: `/var/log/nginx/error.log`  

---

This completes the deployment of your Django project on EC2 with Gunicorn and Nginx. 🎉
