def open_file(f_name):
    books = []
    with open(f_name,"r") as f:
        for line in f:
            el = line.strip().split("    ")
            if len(el) == 3:
                books.append({
                    "author": el[0],
                    "title": el[1],
                    "page": int(el[2])
                })
    return books


def write_file(f_name, data):
    with open(f_name, "w") as f:
        for book in data:
            f.write(f"{book['author']}    {book['title']}    {book['page']}\n")
    return "file is updated"


def get_all_books(data):
    return data


def get_book_by_author(data, author):
    return [book for book in data if book["author"].lower() == author.lower()]


def update_book(data, author, new_title, new_page):
    for book in data:
        if book["author"].lower() == author.lower():
            book["title"] = new_title
            book["page"] = new_page    
            return True
    return False


def delete_book(data, title):
    for book in data:
        if book["title"].lower() == title.lower():
            data.remove(book)
            return data
    return None


def add_book(data, author, title, page):
    data.append({"author": author, "title": title, "page": page})
    return data


def main():
    f_name = "book_data.txt"
    data = open_file(f_name)

    print("all books:", get_all_books(data))

    print( get_book_by_author(data, "name2"))

    add_book(data, "name87", "title445", 450)
    write_file(f_name, data)  
    print("book is added")

    if update_book(data, "name2", "title76", 767):
       write_file(f_name, data)
       print("information is updated")
    else:
     print("book is not found")

    delete_book(data, "title1")
    write_file(f_name, data)  
    print("book is deleted")

if __name__ == "__main__":
    main()
