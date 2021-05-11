FROM yeop2/kogpt2:2

WORKDIR /app
RUN pip install flask requests

COPY . .

EXPOSE 5000

CMD ["python3", "main.py"]
