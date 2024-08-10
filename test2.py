import time

from app.clients.wordnik_client import WordnikClient

start_time = time.time()
word = "gallant"
wordnik_client = WordnikClient(word)
sentences = wordnik_client.extract_example_sentences()
audio_link = wordnik_client.extract_audio_link()
print(f"Done in {time.time() - start_time} seconds")
