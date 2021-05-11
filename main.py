from transformers import GPT2LMHeadModel, PreTrainedTokenizerFast
from flask import Flask, request, jsonify, render_template
import torch
from queue import Queue, Empty
from threading import Thread
import time

app = Flask(__name__)

print("model loading...")

# Model & Tokenizer loading
tokenizer = PreTrainedTokenizerFast.from_pretrained('./KoGPT2',
bos_token='</s>', eos_token='</s>', unk_token='<unk>',
pad_token='<pad>', mask_token='<mask>')
model = GPT2LMHeadModel.from_pretrained('skt/kogpt2-base-v2')

device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
model.to(device)

requests_queue = Queue()    # request queue.
BATCH_SIZE = 1              # max request size.
CHECK_INTERVAL = 0.1

print("complete model loading")


def handle_requests_by_batch():
    while True:
        request_batch = []

        while not (len(request_batch) >= BATCH_SIZE):
            try:
                request_batch.append(requests_queue.get(timeout=CHECK_INTERVAL))
            except Empty:
                continue

            for requests in request_batch:
                try:
                    requests["output"] = make_story(requests['input'][0], requests['input'][1])

                except Exception as e:
                    requests["output"] = e


handler = Thread(target=handle_requests_by_batch).start()


def make_story(text, length):
    try:
        input_ids = tokenizer.encode(text, return_tensors='pt')

        input_ids = input_ids.to(device)

        min_length = len(input_ids.tolist()[0])

        length = length if length > 0 else 1

        length += min_length

        gen_ids = model.generate(input_ids,
                                 max_length=128,
                                 repetition_penalty=2.0,
                                 pad_token_id=tokenizer.pad_token_id,
                                 eos_token_id=tokenizer.eos_token_id,
                                 bos_token_id=tokenizer.bos_token_id,
                                 use_cache=True)

        result = dict()

        for idx, sample_output in enumerate(gen_ids):
            result[0] = tokenizer.decode(sample_output.tolist(), skip_special_tokens=True)
        return result

    except Exception as e:
        print('Error occur in script generating!', e)
        return jsonify({'error': e}), 500


@app.route('/generate', methods=['POST'])
def generate():

    if requests_queue.qsize() > BATCH_SIZE:
        return jsonify({'Error': 'Too Many Requests'}), 429

    try:
        args = []
        text = request.form['text']
        length = int(request.form['length'])

        args.append(text)
        args.append(length)

    except Exception as e:
        return jsonify({'message': 'Invalid request'}), 500

    req = {'input': args}
    requests_queue.put(req)

    while 'output' not in req:
        time.sleep(CHECK_INTERVAL)

    return jsonify(req['output'])


@app.route('/queue_clear')
def queue_clear():
    while not requests_queue.empty():
        requests_queue.get()

    return "Clear", 200


@app.route('/healthz', methods=["GET"])
def health_check():
    return "Health", 200


@app.route('/')
def main():
    return render_template('main.html'), 200


if __name__ == '__main__':
    app.run(port=5000, host='0.0.0.0')
