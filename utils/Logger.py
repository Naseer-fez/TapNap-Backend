from pathlib import Path
import inspect
from datetime import datetime

# def logs(message):
#     filename="DBLogs"
#     path=Path("logs")
#     path.mkdir(exist_ok=True)
#     logging.basicConfig(
        
#         filename=path / f"{filename}.log",
#         filemode='a',
#         format='%(asctime)s - %(levelname)s - %(message)s',
#         level=logging.INFO,
#         force=True)
#     # fromfile= Path(inspect.stack()[1].filename).stem #IF only need the file name 
#     # fromfile = Path(inspect.stack()[1].filename).resolve() # Send the full path
#     fromfile=Path(inspect.stack()[1].filename).resolve().relative_to(Path.cwd()) #Send relative path
#     msg=f"From File {fromfile}-->Error is {message}"
#     logging.error(msg)


def logs(message):
    filename="DBLogs"
    path=Path("logs")
    path.mkdir(exist_ok=True)
    # fromfile= Path(inspect.stack()[1].filename).stem #IF only need the file name 
    # fromfile = Path(inspect.stack()[1].filename).resolve() # Send the full path
    fromfile=Path(inspect.stack()[1].filename).resolve().relative_to(Path.cwd()) #Send relative path
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S,%f")[:-3]
    msg=f"{timestamp} - ERROR - From File {fromfile}-->Error is {message}\n"
    with open(path / f"{filename}.log",'a') as f:
        f.write(msg)