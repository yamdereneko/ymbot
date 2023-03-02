FROM yamdereneko/nb2:1.0

ENV PATH="${PATH}:/root/.local/bin"

ENV LANG=en_US.UTF-8

COPY ./ /app/

WORKDIR /app

RUN chmod a+x start.sh

CMD [ "./start.sh" ]