from mixtral import call_plain, call_explain, call_summary

from flask import Flask, request, jsonify

app = Flask(__name__)

def parse_post(data):
    return data["id"], data["query"]

def parse_get(data):
    return request.args.get('conversation', type=int), request.args.get('query', type=str)

app.route('/favicon.ico')
def serve_favicon():
    return app.send_static_file('favicon.ico')

@app.route('/plain', methods=['POST', 'GET'])
def plain():
    id, query = parse_post(request.json) if request.method == 'POST' else parse_get(request.args)
    response = {
        "id": id,
        "query": query,
        "response": call_plain(query)
    }
    return jsonify(response)

@app.route('/explain_word', methods=['POST', 'GET'])
def explain_word():
    id, query = parse_post(request.json) if request.method == 'POST' else parse_get(request.args)
    response = {
        "id": id,
        "query": query,
        "response": call_explain(query)
    }
    return jsonify(response)

@app.route('/summarize', methods=['POST', 'GET'])
def summarize():
    id, query = parse_post(request.json) if request.method == 'POST' else parse_get(request.args)
    response = {
        "id": id,
        "query": query,
        "response": call_summary(query)
    }
    return jsonify(response)

if __name__ == '__main__':
    app.run(debug=True)
