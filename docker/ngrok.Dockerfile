FROM ngrok/ngrok:latest

# add the ngrok configuration file
COPY ./ngrok/ngrok.yml /etc/ngrok.yml

