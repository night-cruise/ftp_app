# ftp_app

A simple multithreading ftp by socketserver and socket.

## notice

Keep at least one empty dict in `user.db`, otherwise the program will fail.
Just like this: `{}`.

## Installation

clone:

```text
git clone https://github.com/night-cruise/ftp_app.git
cd ftp_app
```

Use the pipenv create & activate virtual env and then install dependency:

```text
pipenv install
pipenv shell
```

run server:

```text
cd server
python run_server.py
```

run client:
```text
cd client
python run_client.py
```

## settings
You can configure Ip and Port in `settings.py`.

## command
- `register username password`: register user.
- `login username password`: login user.
- `cd dirname`: change dir.
- `mkdir dirname`: create dir.
- `dir`: view current dir message.
- `pwd`: view current work dir.
- `get filename`: download file.
- `put filename`: upload file.


## License

This project is licensed under the MIT License (see the
[LICENSE](LICENSE) file for details).
