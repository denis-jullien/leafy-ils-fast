set windows-powershell

hello-windows:
  Write-Host "Hello, world!"
hello-linux:
  echo 'Hello, linux world!'

install:
    pip install -r requirements.txt
    npm install --omit=dev

install-dev:
    pip install -r requirements.txt -r requirements.dev.txt
    npm install

types:
    pydantic2ts --module ./backend/models.py --exclude SQLModelBaseUserDB --exclude User --output ./frontend/src/lib/apiTypes.ts

docker-build:
    docker build -t leafy .

docker-run:
    docker run -p 8000:8000 leafy

ci:
    ruff format backend
    ruff check backend
    pytest backend