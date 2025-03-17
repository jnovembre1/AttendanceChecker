# python runtime for parent image
FROM python:3.9-slim

# working directory
WORKDIR /app

# install dependencies from requirements file
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# idk wtf this does, copys root probably into container
COPY . .

# port for webapp
EXPOSE 8000

# command for docker to boot up webserver
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
