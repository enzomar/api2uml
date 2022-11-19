from flask import Flask, json
from flask import request
from flask import send_file
from flask import render_template
from flask import jsonify


import io

import parser
from umldrawer import UMLDrawer
import base64
import yaml
from plantweb.render import render




api = Flask(__name__)
api.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0



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


@api.route('/uml', methods=['POST'])
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

@api.route('/draw', methods=['POST'])
def draw():
  node = request.args.get('node')
  schemaBase64 = request.form.get('schema')

  base64_bytes = schemaBase64.encode('ascii')
  message_bytes = base64.b64decode(base64_bytes)
  schema = message_bytes.decode('ascii')

  graph, uml = _run(schema, node)
  image = _render_image(uml)

  return _send_file(image)


@api.route('/', methods=['GET'])
def home():
  return render_template('index.html')


if __name__ == '__main__':
    api.run() 