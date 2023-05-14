from flask import Flask, request, jsonify


@app.route('/info', methods=['POST', 'GET', 'HEAD'])
def main():
    if request.method == 'HEAD':
        return ''
    if request.method == 'GET':
        return jsonify({'ok': True})

    # payload = request.get_json()
    # object_name = payload['Records'][0]['s3']['object']['key']
    # bucket_name = payload['Records'][0]['s3']['bucket']['name']
    # my_tasks.task_enqueue_key(bucket_name, object_name)
    return jsonify({'ok': True})
