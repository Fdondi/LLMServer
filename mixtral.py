import mixtral_pb2 as grpc_types, mixtral_pb2_grpc as grpc_services

import grpc
from grpc_health.v1 import health
from grpc_health.v1 import health_pb2
from grpc_health.v1 import health_pb2_grpc
from grpc_reflection.v1alpha import reflection

import logging

from llama_cpp import Llama

from concurrent.futures import ThreadPoolExecutor

dict_instructions="""Premise:
You are Deutsches Wörterbuch, a comprehensive German dictionary designed to adapt its explanations to various levels of German language proficiency, from A1 (beginner) to C2 (native).
You are provided one word, and will first assign it a German level, e.g. B2, then explain it first in German at one level less of difficuly less (in this case B1), then in english.
You'll additionally provide grammatical details, namely:
- for nouns: singular and plural forms with the definite article for the singular.
- for verbs: infinitive, present tense declinations, and past participle. Separable verbs are presented in the infintive with the prefix separated from the root by a double slash // 
- for adjectives: shown with their comparative and superlative forms.
If the word is ambiguous or non-existent, note it and ask for clarification listing at leas three possible similar words.
<s> [INST] nachgeschaut [/INST]
Was: Partizip Perfekt des Verbs (trennbar): nach//schauen
Niveau: B1
Deutsch A2 Erklarung:  Etwas überprüfen oder kontrollieren, indem man einen Blick darauf wirft; sich vergewissern.
Englih explaination: to check, to look up 
Präteritum	ich	schaute nach
Perfekt	Partizip II	nachgeschaut (hilfsverb: haben)
Beispiele:
[1] Er schaute seiner Liebsten noch lange nach.
[2] Schau mal nach, wie weit die Erntehelfer mit der Arbeit sind.
[3] Sie schaut im Fernsehprogramm nach, welche Filme abends laufen.
[3] Unglaublich viele Flexionen kann man detailliert im Wiktionary nachschauen.
[4] Sollen wir vor dem Urlaub das Auto noch in der Werkstatt nachschauen lassen?
</s>
"""

def makePrompt(query, type = grpc_types.TYPE_PLAIN):
	match type:
		case grpc_types.TYPE_PLAIN:
			return f"[INST] {query} [/INST]"
		case grpc_types.TYPE_DICTIONARY:
			return f"{dict_instructions} [INST] {query} [/INST]"


def runLLM(prompt, max_tokens):

	if max_tokens == 0:
		max_tokens = 10000

	# Set gpu_layers to the number of layers to offload to GPU. Set to 0 if no GPU acceleration is available on your system.
	llm = Llama(
		model_path="./mixtral-8x7b-instruct-v0.1.Q4_K_M.gguf",  # Download the model file first
  		n_ctx=2048,  # The max sequence length to use - note that longer sequence lengths require much more resources
  		n_threads=16,            # The number of CPU threads to use, tailor to your system and the resulting performance
  		n_gpu_layers=30         # The number of layers to offload to GPU, if you have GPU acceleration available
	)

	# Simple inference example
	output = llm(
  		prompt, # Prompt
  		max_tokens=max_tokens,  # Generate up to 10000 tokens
  		stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
  		echo=True        # Whether to echo the prompt
	)
	raw_output=output['choices'][0]['text']
	end_instruction_marker = "[/INST]"
	return raw_output[raw_output.rindex(end_instruction_marker)+len(end_instruction_marker):]



class LLMCaller(grpc_services.CallLLM):
	def Call(self, request, context):
		logging.info(f"======================== got request: {request} ========================")
		return grpc_types.Response(
			id = request.id,
			query = request.query,
			response = runLLM(makePrompt(request.query, request.type), request.max_tokens)
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