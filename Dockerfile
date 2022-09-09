FROM nb2:latest

ENV PATH="${PATH}:/root/.local/bin"

ENV LANG=en_US.UTF-8

COPY ./ /app/

WORKDIR /app

CMD [ "python", "./bot.py" ]