from flask import Flask, render_template, request , jsonify , redirect , url_for , flash
from functions.automation import execute_shell_program
from subprocess import run,PIPE,call
from functions.get_docker_images import  get_docker_images
from functions.extract_and_write_content_to_Dockerfile import extract_content_from_response , write_dockerfile
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
from dotenv import load_dotenv
import os

load_dotenv()
genai.configure(api_key=os.environ["API_KEY"])

# Create the model
# See https://ai.google.dev/api/python/google/generativeai/GenerativeModel
generation_config = {
  "temperature": 0.7,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

model = genai.GenerativeModel(
  model_name="gemini-1.5-flash",
  generation_config=generation_config,
  safety_settings={
            HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE
        },
  system_instruction="You Are Jarvis 1.0 , a developer friendly technical assistant to help generate docker file content on the basis of the user's input . User may give required configuration in any format and on the basis of it you have to develop a Docker file. When you Generate a Docker file do not explain the Docker file contents make  it self explanatory using comments inside the Docker file. When User greets you Introduce yourself and explain what is your role",
)

chat_session = model.start_chat()

app = Flask(__name__)

@app.route('/')
def index():
    images = get_docker_images()
    return render_template('index.html',images=images)

@app.route('/select', methods=['POST'])
def select():
    choice = request.form['choice']
    if choice == 'ubuntu':
        message = "You have chosen Ubuntu!"
        msg = execute_shell_program(choice)
    elif choice == 'nginx':
        message = "You have chosen Nginx!"
        msg = execute_shell_program(choice)
    else:
        message = "Invalid choice!"
    
    msg = msg.stdout.replace('\n','<br>')
    return render_template('result.html', message=message , msg=msg)

@app.route('/create_container', methods=['POST'])
def create_container():
    container_choice = request.form['docker_image_choice']
    print(f"container type :: {container_choice}")
    msg = execute_shell_program(container_choice , "auto")
    return render_template('container.html' , message=msg)

# Define a route for the chatbot response
@app.route('/get_response', methods=['POST'])
def get_response():
    user_input = request.form['user_input']
    response = chat_session.send_message(user_input)
    docker_file_content = extract_content_from_response(response.text)
    write_dockerfile(docker_file_content)
    return jsonify(response=response.text)

@app.route('/write_image', methods=['POST'])
def write_image():
    user_input = request.form['write_image']
    write_dockerfile(user_input)
    return redirect(url_for('index'))  # Redirect back to the index page (or wherever your form is)
    
def write_dockerfile(content, output_path="scripts/Dockerfile"):
    with open(output_path, 'w') as file:
        file.write(content)

@app.route('/generate_image' , methods=['POST'])
def build_image():
    name_tag = request.form['image_creation_input']
    result = run(["sh" , "scripts/create_image_using_dockerfile.sh" , name_tag] , stdout=PIPE , text=True)
    print(result)
    return redirect(url_for('index'))

@app.route('/refresh_images', methods=['GET'])
def refresh_images():
    # Fetch the updated list of Docker images here
    images = get_docker_images()  # This function should return the updated list of images
    return jsonify(images=images)

if __name__ == '__main__':
    app.run(debug=True)