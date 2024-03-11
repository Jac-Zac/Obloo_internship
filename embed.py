import ollama
import time

def read_file(file_path):
    """
    Reads the content of a file and decodes it using the 'latin-1' encoding.
    
    Args:
    file_path (str): The path to the file to be read.
    
    Returns:
    str: The content of the file as a string.
    """
    with open(file_path, 'rb') as file:
        return file.read().decode('latin-1')
    

def split_into_chunks(text, chunk_size):
    """
    Splits a given text into chunks of a specified size.
    
    Args:
    text (str): The text to be split into chunks.
    chunk_size (int): The size of each chunk.
    
    Returns:
    list: A list of strings representing the chunks of text.
    """
    words = text.split()
    chunks = []
    current_chunk = []
    
    for word in words:
        current_chunk.append(word)
        if len(current_chunk) >= chunk_size:
            chunks.append(' '.join(current_chunk))
            current_chunk = []
            
    if current_chunk:
        chunks.append(' '.join(current_chunk))
        
    return chunks


file_path = '/Users/sudarshan/Downloads/gpt4all.pdf'
long_string = read_file(file_path)
chunk_size = 2000
chunks = split_into_chunks(long_string, chunk_size)

processed_chunks = 0  # Initialize counter for processed chunks

for i, chunk in enumerate(chunks, start=1):
    if processed_chunks >= 5:  # Stop after processing 5 chunks
        break
    
    start_time = time.time()  # Record start time
    response = ollama.embeddings(model='nomic-embed-text', prompt=chunk)
    #response = ollama.embeddings(model='llama2', prompt=chunk)
    print(i)
    end_time = time.time()  # Record end time
    total_time = end_time - start_time  # Calculate total time
    
    print(f"Total time taken: {total_time:.2f} seconds")
    
    processed_chunks += 1  # Increment processed chunks counter
