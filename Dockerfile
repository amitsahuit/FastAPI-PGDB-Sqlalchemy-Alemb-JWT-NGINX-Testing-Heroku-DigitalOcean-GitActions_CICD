# Docker will cache all the executed steps and if no changes has been done then it will skip all the process and only run the final command.

FROM python:3.9.7

# This will setup a workdirectory in docker
WORKDIR /usr/src/FastAPIDemo

# Incase if the requirements.txt file gets changes then it wil again run from this step till the end and ignoring the above 2 steps.
# Remember the ./ will be the WORKDIR
# if any changes is not there in the requirements.txt file then it wont execute the RUN command for pip install. It will skip it.
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# This command will copy all the src code from local dir to the WORKDIR folder.
COPY . .

# we need to break our command in strings inside the list. this is a kind of syntax docker file uses.
# we can choose any port value as this port value say 80 because this is the port in our docker image..
CMD ["uvicorn", "FastAPIDemo.main:app", "--host", "0.0.0.0", "--port", "8000"]