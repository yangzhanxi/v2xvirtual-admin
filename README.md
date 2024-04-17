# V2X Virtual Admin

This project includes License Management and Network Management for V2X Virtual.


## Backend
### Creating a Dev Enviroment
#### Prerequisites
* Make sure you have a clean Linux distro virtual machine such as Ubuntu.
* Install Python3.10, suggested pyenv.

#### Get the source code
* Clone the repository using Git:
```
git clone git@github.com:yangzhanxi/v2xvirtual-admin.git v2xvirtual-admin
cd v2xvirtual-admin/app
```
#### Dependencies
* Flask
* Flask-Cors
* Flask-JWT-Extended
* Flask-Login
* Flask-Security-Too
* stcrestclient
  
#### Install Dependencies (Ubuntu Linux)
1. Ensure you have a python3.10 installed or install it into your system, using pyenv.
```
pyenv install 3.10.2
pyenv local 3.10.2
```
2. Create a virtual environment for the python dependencies.
```
python -m pip install --upgrade pip
python -m pip install virtualenv
python -m virtualenv ./venv
. ./venv/bin/activate
```
3. Install dependencies.
```
python -m pip install -r requirements.txt # Install flask dependencies
python -m pip install -r test_requirements # Install unit test dependencies
```

#### Run Unit Tests.
```
./run_test.sh
```

#### Run Flask Service
```
python -m falsk run --port=59999 --debug
```

## Frontend
### NPM Dependencies
* React
* React-redux
* SCSS
* orion-rwc

### Install Dependencies
Go to v2xvirtual-admin/webui
```
nvm install && nvm use
npm install
```

### Development
To start development environment run. (To pass API url to backend)
```
npm start -- --env=api='http://localhost:59999/api'
```
Open `http://localhost:8080` on browser.

### Build webui
Go to v2xvirtual-admin/webui
```
nvm use
npm run build
rm -rf ../app/dist
cp -r ./dist ./app/dist
```

## APP Deployment
Go to v2xvirtual-admin
```
tar xvf app.tar ./app
scp app.tar {username}@{ipaddress}/mnt/spirent

#### log in to the remote host ###
cd /mnt/spiernt
tar xvf app.tar
mv app ./v2x-admin
cp v2x-admin/v2xadmin.sh /etc/init.d/v2xadmin
ln -s /etc/init.d/v2xadmin /etc/rc3.d/S99v2xadmin
update-rc.d v2xadmin defaults
```
### Start Service
```
service v2xadmin start
```
### Stop service
```
service v2xadmin stop
```
### Restart service
```
service v2xadmin 
```