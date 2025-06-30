"""
5 Word Frequency Counter: Write a program that analyzes a text file and counts the
frequency of each word. Remove common stop words and punctuation marks to
get more accurate results. Display the top N most frequent words and their
frequencies.
"""

def get_conect(fname):
    try:
        with open(fname, 'r') as f:
            data = f.read()
            return data
    except FileNotFoundError:
        print("file don't found")
        return None

def programm_logic(data, n):
    if data is None:  
        return
    
    stop_words = ["a", "an", "and", "are", "as", "at", "be", "by", "for", "from",
                 "has", "he", "in", "is", "it", "its", "of", "on", "that", "the",
                 "to", "was", "were", "will", "with", "i", "you", "they", "we",
                 "this", "not", "or", "but"]     
    punctuation = ['.', ',', '!', '?', ':', ';', '"', "'", '(', ')', '[', ']', 
                  '{', '}', '-', '_', '—', '…', '/', '\\', '*', '=', '+', '|', '<', '>']
    
    data = data.lower()
    for el in punctuation:
        data = data.replace(el, "")
    
    words = data.split()
    filter_words = [el for el in words if el not in stop_words]  
    
    md = {}
    for word in filter_words:
        if word in md:
            md[word] += 1
        else:
            md[word] = 1
      
    sorted_words = sorted(md.items(), key=lambda item: item[1], reverse=True)
    for w, c in sorted_words[:n]:
        print(w, "---", c)

def main():
    data = get_conect("text.txt")
    programm_logic(data, 5)  

if __name__ == "__main__":
    main()
