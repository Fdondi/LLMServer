import grpc
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc
from grpc_reflection.v1alpha import reflection

import mixtral_pb2 as grpc_types, mixtral_pb2_grpc as grpc_services

import logging
from concurrent.futures import ThreadPoolExecutor

from mixtral import call_plain, call_explain, call_summary

class LLMCaller(grpc_services.CallLLM):
	def Plain(self, request, context):
		logging.info(f"======================== plain request: {request} ========================")
		return grpc_types.Response(
			id = request.id,
			query = request.query,
			response = call_plain(request.query)
		)

	def ExplainWord(self, request, context):
		logging.info(f"======================== explainWord request: {request} ========================")
		return grpc_types.Response(
			id = request.id,
			query = request.query,
			response = call_explain(request.query)
		)

	def Summarize(self, request, context):
		logging.info(f"======================== summary request: {request} ========================")
		return grpc_types.Response(
			id = request.id,
			query = request.query,
			response = call_explain(request.query)
		)

if __name__ == "__main__":
	logging.basicConfig(level=logging.INFO)
	server = grpc.server(ThreadPoolExecutor(max_workers=10))
	grpc_services.add_CallLLMServicer_to_server(LLMCaller(), server)
	# add health check
	health_servicer = health.HealthServicer(
		experimental_non_blocking=True,
		experimental_thread_pool=ThreadPoolExecutor(max_workers=10),
	)
	health_pb2_grpc.add_HealthServicer_to_server(health_servicer, server)
	# add reflection
	SERVICE_NAMES = (
		grpc_types.DESCRIPTOR.services_by_name['CallLLM'].full_name,
		reflection.SERVICE_NAME,
	)
	reflection.enable_server_reflection(SERVICE_NAMES, server)

	# start server
	server.add_insecure_port("[::]:50051")
	server.start()
	print("Server started")
	server.wait_for_termination()