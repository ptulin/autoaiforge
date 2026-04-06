import argparse
import sqlite3
import openai
import os

def initialize_db(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS snippets (
                        id INTEGER PRIMARY KEY,
                        query TEXT,
                        snippet TEXT,
                        tags TEXT
                    )''')
    conn.commit()
    return conn

def query_ai(api_key, prompt):
    openai.api_key = api_key
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=150
        )
        return response.choices[0].text.strip()
    except Exception as e:
        raise RuntimeError(f"Error querying AI: {e}")

def save_snippet(conn, query, snippet, tags):
    cursor = conn.cursor()
    cursor.execute('INSERT INTO snippets (query, snippet, tags) VALUES (?, ?, ?)', (query, snippet, tags))
    conn.commit()

def retrieve_snippets(conn, tags):
    cursor = conn.cursor()
    cursor.execute('SELECT id, query, snippet, tags FROM snippets WHERE tags LIKE ?', (f"%{tags}%",))
    return cursor.fetchall()

def main():
    parser = argparse.ArgumentParser(description="AI Assistant Snippet Manager")
    parser.add_argument('--query', type=str, help='Query to send to the AI assistant')
    parser.add_argument('--save', action='store_true', help='Save the generated snippet')
    parser.add_argument('--tags', type=str, help='Comma-separated tags for the snippet')
    parser.add_argument('--retrieve', type=str, help='Retrieve snippets by tags')
    parser.add_argument('--api-key', type=str, help='OpenAI API key', required=True)
    parser.add_argument('--db-path', type=str, default='snippets.db', help='Path to the SQLite database')

    args = parser.parse_args()

    conn = initialize_db(args.db_path)

    if args.query:
        snippet = query_ai(args.api_key, args.query)
        print("Generated Snippet:")
        print(snippet)
        if args.save:
            if not args.tags:
                print("Error: --tags is required when using --save")
                return
            save_snippet(conn, args.query, snippet, args.tags)
            print("Snippet saved successfully.")

    if args.retrieve:
        snippets = retrieve_snippets(conn, args.retrieve)
        if snippets:
            print("Retrieved Snippets:")
            for snippet in snippets:
                print(f"ID: {snippet[0]}, Query: {snippet[1]}, Tags: {snippet[3]}\n{snippet[2]}\n")
        else:
            print("No snippets found for the given tags.")

if __name__ == "__main__":
    main()