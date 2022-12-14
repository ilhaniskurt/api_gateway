import argparse
from socket import gethostname
import uvicorn

DEFAULT_IP = "127.0.0.1"
DEFAULT_PORT = 8000
DEFAULT_BIND = f"{DEFAULT_IP}:{DEFAULT_PORT}"
DEFAULT_APP = "api.main:app"

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=f"Python script to launch web app. Default API instance {DEFAULT_APP} Using default value for hosting address: {DEFAULT_BIND}")
    group = parser.add_mutually_exclusive_group()
    #subparser = parser.add_subparsers(dest="command")

    parser.add_argument("app", default=DEFAULT_APP, nargs="?",
        help="Module location and the name of the API instance")

    parser.add_argument("--reload", default=False, action="store_true", 
        help="Reload the server on changes")

    group.add_argument("--bind", default=DEFAULT_BIND, type=str, 
        help="Enter ip address and port to host on e.g: 127.0.0.1:8000")
    group.add_argument("--local", const=DEFAULT_PORT, nargs="?", type=int, 
        help="Host the server on local IPv4 with default port unless specified")

    args = parser.parse_args()

    if args.local:
        uvicorn.run(args.app, host=gethostname(), port=args.local, reload=args.reload)
    else:
        bind = args.bind.split(":")
        uvicorn.run(args.app, host=bind[0], port=int(bind[1]), reload=args.reload)