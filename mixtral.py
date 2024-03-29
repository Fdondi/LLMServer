from html import escape

from llama_cpp import Llama

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

summary_instructions = """Summarize
<s> [INST] The global tech industry has seen a significant shift towards green technology in recent years. Companies are investing heavily in renewable energy sources, such as solar and wind power, to reduce their carbon footprint. This trend is driven by increasing awareness of climate change and the need for sustainable development. Major tech giants have announced plans to become carbon neutral within the next decade. Initiatives include improving energy efficiency in data centers, using recycled materials in products, and investing in environmental restoration projects. Governments around the world are also supporting this shift by offering tax incentives and subsidies for green technology investments. Despite these positive steps, challenges remain, including the high initial cost of transitioning to green technology and the need for more widespread consumer adoption. However, the long-term benefits, including reduced environmental impact and lower operational costs, make this a worthwhile investment for the tech industry.[/INST]
The global tech industry is rapidly embracing green technology, driven by the goal of reducing carbon emissions and achieving sustainability. Despite challenges like high initial costs, the move is supported by government incentives and promises long-term environmental and economic benefits.
</s>

"""


def wrapPrompt(query):
	sanitized_query = escape(query)
	return f"[INST] {sanitized_query} [/INST]"

def runLLM(prompt):

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
  		max_tokens=10000,  # Generate up to 10000 tokens
  		stop=["</s>"],   # Example stop token - not necessarily correct for this specific model! Please check before using.
  		echo=True        # Whether to echo the prompt
	)
	raw_output=output['choices'][0]['text']
	end_instruction_marker = "[/INST]"
	return raw_output[raw_output.rindex(end_instruction_marker)+len(end_instruction_marker):]

def call_plain(query):
	return runLLM(wrapPrompt(query))

def call_explain(query):
	return runLLM(dict_instructions + wrapPrompt(query))

def call_summary(query):
	return runLLM(summary_instructions + wrapPrompt(query))