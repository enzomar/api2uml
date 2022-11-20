from flask import Flask, json
from flask import request
from flask import send_file
from flask import render_template
from flask import jsonify
from datetime import datetime


import platform,socket,re,uuid,json,psutil,logging


import io

import parser
from umldrawer import UMLDrawer
import base64
import yaml
from plantweb.render import render


app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["TEMPLATES_AUTO_RELOAD"] = True


def _load(schema):
  spec = None
  try:
    spec = yaml.safe_load(schema)
  except yaml.YAMLError as exc:
    print(exc)
  return spec 


def _render_image(uml):
  image = render(
        uml,
        server='http://localhost:8080',
        engine='plantuml',
        format='png')
  return image


def _run(schema, node_name=None):

  spec = _load(schema)
  graph = parser.parse(spec)

  ud = UMLDrawer()
  uml = ud.to_plantuml(graph, node_name)

  return graph, uml



def _send_file(image_data):
  mem = io.BytesIO()

  image_raw = image_data[0]
  extension = image_data[1]


  mem.write(image_raw)
  # seeking was necessary. Python 3.5.2, Flask 0.12.2
  mem.seek(0)

  return send_file(
      mem,
      as_attachment=True,
      download_name='output.png',
      mimetype='image/gif'
  )


def _get_size(bytes, suffix="B"):
    """
    Scale bytes to its proper format
    e.g:
        1253656 => '1.20MB'
        1253656678 => '1.17GB'
    """
    factor = 1024
    for unit in ["", "K", "M", "G", "T", "P"]:
        if bytes < factor:
            return f"{bytes:.2f}{unit}{suffix}"
        bytes /= factor

def _get_info():

  print("="*40, "System Information", "="*40)
  uname = platform.uname()
  print(f"System: {uname.system}")
  print(f"Node Name: {uname.node}")
  print(f"Release: {uname.release}")
  print(f"Version: {uname.version}")
  print(f"Machine: {uname.machine}")
  print(f"Processor: {uname.processor}")

  # Boot Time
  print("="*40, "Boot Time", "="*40)
  boot_time_timestamp = psutil.boot_time()
  bt = datetime.fromtimestamp(boot_time_timestamp)
  print(f"Boot Time: {bt.year}/{bt.month}/{bt.day} {bt.hour}:{bt.minute}:{bt.second}")

  # let's print CPU information
  print("="*40, "CPU Info", "="*40)
  # number of cores
  print("Physical cores:", psutil.cpu_count(logical=False))
  print("Total cores:", psutil.cpu_count(logical=True))
  # CPU frequencies
  cpufreq = psutil.cpu_freq()
  print(f"Max Frequency: {cpufreq.max:.2f}Mhz")
  print(f"Min Frequency: {cpufreq.min:.2f}Mhz")
  print(f"Current Frequency: {cpufreq.current:.2f}Mhz")
  # CPU usage
  print("CPU Usage Per Core:")
  for i, percentage in enumerate(psutil.cpu_percent(percpu=True, interval=1)):
      print(f"Core {i}: {percentage}%")
  print(f"Total CPU Usage: {psutil.cpu_percent()}%")

  # Memory Information
  print("="*40, "Memory Information", "="*40)
  # get the memory details
  svmem = psutil.virtual_memory()
  print(f"Total: {_get_size(svmem.total)}")
  print(f"Available: {_get_size(svmem.available)}")
  print(f"Used: {_get_size(svmem.used)}")
  print(f"Percentage: {svmem.percent}%")
  print("="*20, "SWAP", "="*20)
  # get the swap memory details (if exists)
  swap = psutil.swap_memory()
  print(f"Total: {_get_size(swap.total)}")
  print(f"Free: {_get_size(swap.free)}")
  print(f"Used: {_get_size(swap.used)}")
  print(f"Percentage: {swap.percent}%")

  # Disk Information
  print("="*40, "Disk Information", "="*40)
  print("Partitions and Usage:")
  # get all disk partitions
  partitions = psutil.disk_partitions()
  for partition in partitions:
      print(f"=== Device: {partition.device} ===")
      print(f"  Mountpoint: {partition.mountpoint}")
      print(f"  File system type: {partition.fstype}")
      try:
          partition_usage = psutil.disk_usage(partition.mountpoint)
      except PermissionError:
          # this can be catched due to the disk that
          # isn't ready
          continue
      print(f"  Total Size: {_get_size(partition_usage.total)}")
      print(f"  Used: {_get_size(partition_usage.used)}")
      print(f"  Free: {_get_size(partition_usage.free)}")
      print(f"  Percentage: {partition_usage.percent}%")
  # get IO statistics since boot
  disk_io = psutil.disk_io_counters()
  print(f"Total read: {_get_size(disk_io.read_bytes)}")
  print(f"Total write: {_get_size(disk_io.write_bytes)}")

  # Network information
  print("="*40, "Network Information", "="*40)
  # get all network interfaces (virtual and physical)
  if_addrs = psutil.net_if_addrs()
  for interface_name, interface_addresses in if_addrs.items():
      for address in interface_addresses:
          print(f"=== Interface: {interface_name} ===")
          if str(address.family) == 'AddressFamily.AF_INET':
              print(f"  IP Address: {address.address}")
              print(f"  Netmask: {address.netmask}")
              print(f"  Broadcast IP: {address.broadcast}")
          elif str(address.family) == 'AddressFamily.AF_PACKET':
              print(f"  MAC Address: {address.address}")
              print(f"  Netmask: {address.netmask}")
              print(f"  Broadcast MAC: {address.broadcast}")
  # get IO statistics since boot
  net_io = psutil.net_io_counters()
  print(f"Total Bytes Sent: {_get_size(net_io.bytes_sent)}")
  print(f"Total Bytes Received: {_get_size(net_io.bytes_recv)}")

def _get_system_info():
    try:
      _get_info()
    except Exception as e:
      print(str(e))

    try:
        info={}
        info['platform']=platform.system()
        info['platform-release']=platform.release()
        info['platform-version']=platform.version()
        info['architecture']=platform.machine()
        info['hostname']=socket.gethostname()
        info['ip-address']=socket.gethostbyname(socket.gethostname())
        info['mac-address']=':'.join(re.findall('..', '%012x' % uuid.getnode()))
        info['processor']=platform.processor()
        info['processor usage %']=psutil.cpu_percent()
        info['ram (total)']=str(round(psutil.virtual_memory().total / (1024.0 **3)))+" GB"
        info['ram (used)']=str(round(psutil.virtual_memory().used / (1024.0 **3)))+" GB"

        return info
    except Exception as e:
        print(str(e))

@app.route('/info', methods=['GET'])
def info():
  info = _get_system_info()
  return jsonify(info)


@app.route('/uml', methods=['POST'])
def uml():
  body = request.json
  schemaBase64 = body['schema']
  node = request.args.get('node')


  if not schemaBase64:
    return '',400

  base64_bytes = schemaBase64.encode('ascii')
  message_bytes = base64.b64decode(base64_bytes)
  schema = message_bytes.decode('ascii')

  graph, uml = _run(schema, node)

  output = dict()
  output['nodes'] = []
  for each in graph.nodes:
    output['nodes'].append(each)
  output['uml'] = base64.b64encode(uml.encode('ascii')).decode('utf-8')

  return jsonify(output)

@app.route('/draw', methods=['POST'])
def draw():
  node = request.args.get('node')
  schemaBase64 = request.form.get('schema')

  base64_bytes = schemaBase64.encode('ascii')
  message_bytes = base64.b64decode(base64_bytes)
  schema = message_bytes.decode('ascii')

  graph, uml = _run(schema, node)
  image = _render_image(uml)

  return _send_file(image)





@app.route('/', methods=['GET'])
def home():
  return render_template('index.html')


if __name__ == '__main__':
    app.run() 