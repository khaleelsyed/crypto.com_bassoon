import websocket
import _thread
import time
import json


def on_message(ws, message):
	json_msg = json.loads(message)
	
	if json_msg['method'] == 'public/heartbeat':
		handle_heartbeat(json_msg['id'])
	
	# Response to a subscription
	elif json_msg['method'] == 'subscribe':
		handle_subscribed(json_msg)

	
def on_error(ws, err_message):
	print(err_message)

	
def on_close(ws, close_code, close_msg):
	if close_code == 1000:
		print('CLOSED: 1000 -> Probably did not respond to heartbeat')
	else:
		print(f'Closed: {close_code}\n{close_msg}')


def on_open(ws):
	def run(*args):
		# Run for 60 seconds
		for i in range(60):
			time.sleep(1)
			# ws.send(f'Hello {i}')
		time.sleep(1)
		ws.close()
		print('Thread Terminating')
	_thread.start_new_thread(run, ())


def handle_heartbeat(id):
	response = '{' + f'"id": {id}, "method": "public/respond-heartbeat"' + '}'
	ws.send(response)


def handle_subscription(message):
	pass


def subscribe(subscription):
	
	# TODO: Generate a new ID
	
	response = '{' + f'"id": {id}' + ', "method": "subscribe"' + '"params": {}' '}'
	ws.send(response)


def unsubscribe(subscription):
	pass


if __name__ == '__main__':
	websocket.enableTrace(True)
	ws = websocket.WebSocketApp('wss://uat-stream.3ona.co/v2/market', on_open=on_open, on_message=on_message, on_error=on_error, on_close=on_close)
	ws.run_forever()
