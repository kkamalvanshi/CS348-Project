import sqlite3

# Replace 'your_database_file.db' with the path to your actual SQLite database file.
DATABASE_FILE = 'instance/database1.db'

def get_top_servers(top_x):
    # Connect to the SQLite database
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()

        # SQL query to retrieve the top servers by number of model deployments
        query = """
        SELECT s.name, COUNT(md.id) AS deployments_count
        FROM server s
        JOIN model_deployment md ON s.id = md.server_id
        GROUP BY s.name
        ORDER BY deployments_count DESC
        LIMIT ?
        """

        cursor.execute(query, (top_x,))
        rows = cursor.fetchall()

    return rows

def main():
    top_x = int(input("Enter the number of top servers to fetch: "))
    top_servers = get_top_servers(top_x)
    
    # Print the results
    print("Top servers based on the number of deployments:")
    for server_name, count in top_servers:
        print(f"Server Name: {server_name}, Deployments: {count}")

if __name__ == "__main__":
    main()
