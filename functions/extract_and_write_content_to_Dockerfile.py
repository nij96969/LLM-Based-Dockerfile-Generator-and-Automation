def extract_content_from_response(response_text):
    start_index = response_text.find("```dockerfile") + len("```dockerfile") + 1
    end_index = response_text.find("```", start_index)

    extracted_content = response_text[start_index:end_index]

    return extracted_content

def write_dockerfile(content, output_path="./scripts/Dockerfile"):
    with open(output_path, 'w') as file:
        file.write(content)