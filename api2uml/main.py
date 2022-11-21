from flask import Flask, json
from flask import request
from flask import send_file
from flask import render_template
from flask import jsonify
from utils.inspector import Inspector
import systeminfo
from parser import parser
from utils.umldrawer import UMLDrawer
import model.graph
import base64
import yaml
from plantweb.render import render

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["TEMPLATES_AUTO_RELOAD"] = True

@app.route('/info', methods=['GET'])
def info():
  info = systeminfo._get_system_info()
  return jsonify(info)



def _run_from_graph(in_graph, node_name=None):
  ud = UMLDrawer()
  uml = ud.to_plantuml(in_graph, node_name)
  return uml

def _load(schema):
  spec = None
  try:
    spec = yaml.safe_load(schema)
  except yaml.YAMLError as exc:
    print(exc)
  return spec 

def _run(schema, node_name=None):
  spec = _load(schema)
  in_graph = parser.parse(spec)
  uml = _run_from_graph(in_graph, node_name=None)

  return in_graph, uml

def _prepare_reply(loc_graph, uml):
    output = dict()
    output['nodes'] = []
    for each in loc_graph.nodes:
      output['nodes'].append(each)
    output['nodes'].sort()
    output['uml'] = base64.b64encode(uml.encode('ascii')).decode('utf-8')
    output['inspect'] = Inspector.inspect(loc_graph)
    output['graph'] = loc_graph.serialize()
    return output


def _decode_schema(schemaBase64):
  base64_bytes = schemaBase64.encode('ascii')
  message_bytes = base64.b64decode(base64_bytes)
  return message_bytes.decode('ascii')


@app.route('/uml', methods=['POST'])
def uml():
  body = request.json
  schemaBase64 = body['schema']
  if not schemaBase64:
    return '',400

  schema = _decode_schema(schemaBase64)
  node_name = request.args.get('node')
  
  loc_graph, uml =  None, None

  try: 
    #print("Try to deserialize graph")
    serialized_graph = body['graph']
    loc_graph = model.graph.deserialize(serialized_graph)
    uml = _run_from_graph(loc_graph, node_name)
  except Exception as ex:
    print(str(ex))
    #print("If fails rebuild the graph from the shema")
    try:
      loc_graph, uml = _run(schema, node_name)
    except Exception as ex2:
      print(str(ex2))
  finally:
    output = _prepare_reply(loc_graph, uml)
    return jsonify(output)


@app.route('/', methods=['GET'])
def home():
  return render_template('index.html')


if __name__ == '__main__':
    app.run() 