# Camlin Test
<br>

## RUN CONTAINERIZED VERSION

Running containerized version is pretty simple.<br>
Clone the code and in the root of the project run

***docker build -t camlin_test .***

and

***docker run -p 8080:8080 camlin_test***

If evrething is ok, you should access to the API with<br>
http://127.0.0.1:8080/docs
<br><br>

## RUN ON LOCAL COMPUTER

Clone the code.<br>
In the root of the project create virtual env.

***python -m venv .venv***

Activate virtual env.

***source .venv/bin/activate***

Install from requirements.txt.

***pip install -r requirements.txt***

Run FastAPI.

***fastapi dev main.py***

If evrething is ok, you should access to the API with<br>
http://127.0.0.1:8000/docs
