import sqlite3
from datetime import datetime

DATABASE_FILE = 'instance/database1.db'

def generate_deployment_report(start_date, end_date, model_type=None):
    with sqlite3.connect(DATABASE_FILE) as conn:
        cursor = conn.cursor()

        # Convert MMDD to datetime format for filtering
        start_date_str = f"{str(start_date)[:2]}/{str(start_date)[2:4]}/2024"
        end_date_str = f"{str(end_date)[:2]}/{str(end_date)[2:4]}/2024"
        start_date_dt = datetime.strptime(start_date_str, "%m/%d/%Y")
        end_date_dt = datetime.strptime(end_date_str, "%m/%d/%Y")

        # Construct the SQL query dynamically based on model type
        query = """
        SELECT md.id, s.name as server_name, m.name as model_name, md.deployment_time
        FROM model_deployment md
        JOIN version v ON md.version_id = v.id
        JOIN model m ON v.model_id = m.id
        JOIN server s ON md.server_id = s.id
        WHERE md.deployment_time BETWEEN ? AND ?
        """
        params = [start_date_dt, end_date_dt]

        if model_type:
            query += " AND m.type = ?"
            params.append(model_type)

        cursor.execute(query, params)
        result = cursor.fetchall()

        # Format the result for display
        report_data = {
            'total_deployments': len(result),
            'deployments': [
                {
                    'id': row[0],
                    'server_name': row[1],
                    'model_name': row[2],
                    'deployment_time': datetime.strptime(str(row[3]), '%Y%m%d').strftime("%m/%d/%Y") if row[3] else "Not Available"
                } for row in result
            ]
        }

        return report_data

def main():
    start_date = input("Enter start date (MMDD): ")
    end_date = input("Enter end date (MMDD): ")
    model_type = input("Enter model type (leave blank if not filtering by model type): ")

    report = generate_deployment_report(start_date, end_date, model_type)
    
    # Print the report
    print(f"Total deployments: {report['total_deployments']}")
    for deployment in report['deployments']:
        print(f"ID: {deployment['id']}, Server: {deployment['server_name']}, Model: {deployment['model_name']}, Date: {deployment['deployment_time']}")

if __name__ == "__main__":
    main()
