import streamlit as st
import requests
from datetime import datetime

# Base URL of your Flask app
BASE_URL = "http://127.0.0.1:5000"

st.title('Model Deployment Service')

def get_data(endpoint, params=None):
    """
    Fetch data from a specified endpoint. Optionally include query parameters.

    Args:
    - endpoint (str): The endpoint to fetch data from.
    - params (dict, optional): A dictionary of query parameters.

    Returns:
    - JSON response data if the request is successful, otherwise an empty list.
    """
    if params is None:
        response = requests.get(f"{BASE_URL}/{endpoint}")
    else:
        response = requests.get(f"{BASE_URL}/{endpoint}", params=params)
    
    return response.json() if response.status_code == 200 else []

def update_data(endpoint, data):
    """Function to update data on the backend."""
    response = requests.put(f"{BASE_URL}/{endpoint}", json=data)
    return response.status_code


def post_data(endpoint, data):
    """Function to post data to the backend."""
    response = requests.post(f"{BASE_URL}/{endpoint}", json=data)
    return response.status_code == 201

def delete_data(endpoint, item_id):
    """Function to delete data from the backend."""
    response = requests.delete(f"{BASE_URL}/{endpoint}/{item_id}")
    return response.status_code == 200
# Sidebar for navigation
st.sidebar.title("Navigation")
options = ["Models","Datasets", "Versions", "Servers", "Deployments", "Deployment Reports", "Top Servers Report", "Model Types Count"]
choice = st.sidebar.radio("Choose an option", options)

if choice == "Models":
    st.subheader('Model Management')

    # Add Model
    with st.form("add_model"):
        name = st.text_input("Model Name")
        description = st.text_area("Model Description")
        model_type = st.selectbox("Model Type", ["LLM", "Regression", "Neural Network", "Other"])  # Added dropdown for model type
        submit_button = st.form_submit_button("Add Model")
        if submit_button:
            model_data = {
                'name': name,
                'description': description,
                'type': model_type  # Include the model type in the data sent to the backend
            }
            if post_data('models', model_data):
                st.success("Model added successfully")
            else:
                st.error("Failed to add model")


    # List Models
    models = get_data('models')
    model_type = st.selectbox("Model Type", ["All", "LLM", "Regression", "Neural Network"])
    if model_type != "All":
        models = [model for model in models if model['type'] == model_type]
    for model in models:
        st.text(f"ID: {model['id']} - Name: {model['name']} - Type: {model['type']} - Description: {model['description']}")
        if st.button("Delete", key=f"delete_model_{model['id']}"):
            if delete_data('models', model['id']):
                st.success(f"Model {model['id']} deleted")
            else:
                st.error(f"Failed to delete model {model['id']}")

elif choice == "Datasets":
    st.subheader('Dataset Management')

    # Add Dataset Form
    with st.form("add_dataset"):
        name = st.text_input("Dataset Name")
        description = st.text_area("Dataset Description")
        data_type = st.selectbox("Data Type", ["text", "image", "video", "audio"])
        submit_button = st.form_submit_button("Add Dataset")
        if submit_button:
            if post_data('datasets', {'name': name, 'description': description, 'data_type': data_type}):
                st.success("Dataset added successfully")
            else:
                st.error("Failed to add dataset")

    # List Datasets
    datasets = get_data('datasets')
    for dataset in datasets:
        st.text(f"ID: {dataset['id']} - Name: {dataset['name']} - Description: {dataset['description']} - Type: {dataset['data_type']}")
        if st.button("Delete", key=f"delete_dataset_{dataset['id']}"):
            if delete_data('datasets', dataset['id']):
                st.success(f"Dataset {dataset['id']} deleted")
            else:
                st.error(f"Failed to delete dataset {dataset['id']}")

    # Update and other operations go here

elif choice == "Versions":
    st.subheader('Version Management')

    # Add Version Form
    with st.form("add_version"):
        model_id = st.number_input("Model ID", step=1)
        dataset_id = st.number_input("Dataset ID", step=1)
        version_number = st.text_input("Version Number")
        performance_metrics = st.text_area("Performance Metrics")
        submit_button = st.form_submit_button("Add Version")
        if submit_button:
            if post_data('versions', {'model_id': model_id, 'dataset_id': dataset_id, 'version_number': version_number, 'performance_metrics': performance_metrics}):
                st.success("Version added successfully")
            else:
                st.error("Failed to add version")

    # List Versions
    versions = get_data('versions')
    for version in versions:
        st.text(f"ID: {version['id']} - Model ID: {version['model_id']} - Dataset ID: {version['dataset_id']} - Version Number: {version['version_number']} - Metrics: {version['performance_metrics']}")
        if st.button("Delete", key=f"delete_version_{version['id']}"):
            if delete_data('versions', version['id']):
                st.success(f"Version {version['id']} deleted")
            else:
                st.error(f"Failed to delete version {version['id']}")

    # Update and other operations go here


elif choice == "Servers":
    st.subheader('Server Management')

    # Add Server Form
    with st.form("add_server"):
        name = st.text_input("Server Name")
        ip_address = st.text_input("IP Address")
        submit_button = st.form_submit_button("Add Server")
        if submit_button:
            if post_data('servers', {'name': name, 'ip_address': ip_address}):
                st.success("Server added successfully")
            else:
                st.error("Failed to add server")

    # List Servers
    servers = get_data('servers')
    for server in servers:
        st.text(f"ID: {server['id']} - Name: {server['name']} - IP Address: {server['ip_address']}")
        if st.button("Delete", key=f"delete_server_{server['id']}"):
            if delete_data('servers', server['id']):
                st.success(f"Server {server['id']} deleted")
            else:
                st.error(f"Failed to delete server {server['id']}")

    # Update and other operations go here


elif choice == "Deployments":
    st.subheader('Deployment Management')

    # Add Deployment Form
    with st.form("add_deployment"):
        server_id = st.number_input("Server ID", step=1)
        version_id = st.number_input("Version ID", step=1)
        deployment_date = st.number_input("Deployment Date (MMDD)", min_value=101, max_value=1231, step=1)

        submit_button = st.form_submit_button("Add Deployment")
        if submit_button:
            deployment_data = {'server_id': server_id, 'version_id': version_id, 'deployment_time': deployment_date}
            if post_data('modeldeployments', deployment_data):
                st.success("Deployment added successfully.")
                st.experimental_rerun()
            else:
                st.error("Failed to add deployment.")

    # List Deployments
    st.subheader("Current Deployments")
    deployments = get_data('modeldeployments')
    if deployments:
        for deployment in deployments:
            # Formatting MMDD integer for display
            deployment_date_str = f"{str(deployment['deployment_time'])[:-2]}/{str(deployment['deployment_time'])[-2:]}"
            st.write(f"ID: {deployment['id']} - Server ID: {deployment['server_id']} - Version ID: {deployment['version_id']} - Deployment Date: {deployment_date_str}")
            if st.button("Delete", key=f"delete_{deployment['id']}"):
                if delete_data('modeldeployments', deployment['id']):
                    st.success(f"Successfully deleted deployment {deployment['id']}")
                    st.experimental_rerun()
                else:
                    st.error("Failed to delete deployment.")
    else:
        st.write("No deployments found.")
elif choice == "Deployment Reports":
    st.subheader('Deployment Reports by Name and Server')

    start_date = st.number_input("Start Date (MMDD)", min_value=101, max_value=1231, step=1, format='%d')
    end_date = st.number_input("End Date (MMDD)", min_value=101, max_value=1231, step=1, format='%d')
    
    # Assuming this part fetches model types successfully from another function
    model_type_options = ["All"] + [model['type'] for model in get_data('models')]
    selected_model_type = st.selectbox("Model Type", model_type_options)

    if st.button("Generate Report"):
        params = {"start_date": start_date, "end_date": end_date}
        if selected_model_type != "All":
            params["model_type"] = selected_model_type
            
        report_data = get_data('reports/deployments', params=params)

        if report_data:
            st.write("Deployments Matching Criteria:")
            for deployment in report_data["deployments"]:
                st.write(deployment)
    
        else:
            st.error("No data found for selected filters.")
elif choice == "Top Servers Report":
    st.subheader("Top Servers Deploying the Most Models")
    top_x = st.number_input("Enter number of top servers to fetch", min_value=1, value=5)
    if st.button("Show Top Servers"):
        top_servers = get_data("reports/top-servers", params={"top": top_x})
        if top_servers:
            for server in top_servers:
                st.text(f"Server Name: {server['server_name']} - Deployments Count: {server['deployments_count']}")
        else:
            st.error("Failed to fetch top servers report.")


elif choice == "Update Model":
    st.subheader("Update an Existing Model")

    # Fetch all models to populate the selection box
    models = get_data('models')
    model_names = {model['name']: model['id'] for model in models}
    selected_model_name = st.selectbox("Select a model to update", options=list(model_names.keys()))

    if selected_model_name:
        selected_model_id = model_names[selected_model_name]
        # Fetch details of the selected model
        selected_model_details = next((model for model in models if model['id'] == selected_model_id), None)

        if selected_model_details:
            # Display model details for editing
            name = st.text_input("Model Name", value=selected_model_details['name'])
            description = st.text_area("Description", value=selected_model_details['description'])
            model_type = st.selectbox("Type", options=["LLM", "Regression", "Neural Network", "Other"], index=["LLM", "Regression", "Neural Network", "Other"].index(selected_model_details['type']))

            if st.button(f"Update Model #{selected_model_id}"):
                updated_data = {
                    'name': name,
                    'description': description,
                    'type': model_type
                }
                response = update_data(f'models/{selected_model_id}', updated_data)
                print("Update response:", response)  # Temporary debug print
                if response == 200:
                    st.success("Model updated successfully.")
                else:
                    st.error(f"Failed to update model. Response code: {response}")

elif choice == "Model Types Count":
    st.subheader("Model Types Deployment Count")

    # Fetching model types count data from the Flask backend
    model_types_count = get_data("reports/model-types-count")

    if model_types_count:
        # Displaying each model type with its deployment count
        for item in model_types_count:
            st.write(f"Model Type: {item['type']} - Deployments: {item['count']}")
    else:
        st.write("No data found.")
