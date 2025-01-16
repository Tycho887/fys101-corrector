import os
from openai import OpenAI
from dotenv import load_dotenv

# Load the OpenAI API key from the environment

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")


def load_file(file_path):
    """Reads and returns the content of a file."""
    with open(file_path, 'r') as file:
        return file.read()


def save_file(file_path, content):
    """Saves the provided content to a file."""
    with open(file_path, 'w') as file:
        file.write(content)


def split_problems(content, marker="MARKPROB"):
    """Splits LaTeX content into problems using a marker."""
    return content.split(marker)[1:]  # Exclude preamble part


def wrap_document(preamble, problems, postamble):
    """Wraps the problems with global LaTeX structure."""
    return f"""{preamble}
{problems}
{postamble}
"""


def load_formatting(directory="formating/"):
    """Loads formatting components (preamble, postamble, prompt) from files."""
    preamble = load_file(os.path.join(directory, "preamble.txt"))
    postamble = load_file(os.path.join(directory, "postamble.txt"))
    prompt = load_file(os.path.join(directory, "prompt.txt"))
    return preamble, postamble, prompt


def correct_problem(problem_text, prompt_start):
    """
    Corrects a problem using the OpenAI GPT-4 model.

    Args:
        problem_text (str): The text of the problem to be corrected.
        prompt_start (str): The initial part of the prompt to guide the correction.

    Returns:
        str: The corrected problem text if successful; otherwise, the original problem text.
    """
    from openai import OpenAI

    client = OpenAI(api_key=api_key)

    # Construct the prompt for the model
    prompt = f"""
    {prompt_start}

    # Problem:
    {problem_text}

    Corrected Problem:
    """

    try:
        # Generate the response using the GPT-4 model
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": prompt}],
            max_tokens=2500,
            temperature=0.2,
        )

        # Return the content of the first choice
        return response.choices[0].message.content

    except Exception as e:
        # Handle exceptions and return the original problem text
        print(f"Error correcting problem: {e}")
        return problem_text


def postprocess_content(content):
    """
    Removes known artifacts from the content, such as markdown code blocks and LaTeX delimiters.

    Args:
        content (str): The content to be post-processed.

    Returns:
        str: The cleaned content.
    """
    artifacts = [
        "```latex",       # LaTeX-specific code block delimiter
        "```",            # Markdown code block delimiter
    ]

    # Remove each artifact from the content
    for artifact in artifacts:
        content = content.replace(artifact, "")

    return content


def process_latex_content(latex_content, preamble, postamble, prompt, marker="MARKPROB"):
    """Processes LaTeX content by correcting individual problems."""
    problems = split_problems(latex_content, marker)

    corrected_problems = []
    for i, problem in enumerate(problems):
        print(f"Processing problem {i + 1}/{len(problems)}...")
        corrected = correct_problem(problem.strip(), prompt)
        cleaned_corrected = postprocess_content(corrected)
        corrected_problems.append(cleaned_corrected)

    all_problems = "\n\n".join(corrected_problems)
    return wrap_document(preamble, all_problems, postamble)


def process_files_in_directory(input_dir="inputs", output_dir="output", marker="MARKPROB"):
    """Processes all .tex files in the input directory and saves two versions of results to the output directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    preamble, postamble, prompt = load_formatting()

    for file_name in os.listdir(input_dir):
        if file_name.endswith(".tex"):
            input_path = os.path.join(input_dir, file_name)

            # Create subdirectory for the output files inside the output directory

            sub_dir = file_name.split(".")[0]

            if not os.path.exists(os.path.join(output_dir, sub_dir)):
                os.makedirs(os.path.join(output_dir, sub_dir))

            output_path_1 = os.path.join(output_dir, sub_dir, f"{file_name.split('.')[0]}_corrected_1.tex")
            # output_path_2 = os.path.join(output_dir, sub_dir, f"{file_name.split('.')[0]}_corrected_2.tex")

            print(f"Processing file: {file_name}...")
            latex_content = load_file(input_path)

            # Generate the first corrected version
            # print("Processing version 1...")
            corrected_content_1 = process_latex_content(latex_content, preamble, postamble, prompt, marker)

            # # Generate the second corrected version (e.g., with a different temperature or approach if desired)
            # print("Processing version 2...")
            # corrected_content_2 = process_latex_content(latex_content, preamble, postamble, prompt, marker)

            # Save both versions
            save_file(output_path_1, corrected_content_1)
            print(f"Saved corrected file version 1 to: {output_path_1}")

            # save_file(output_path_2, corrected_content_2)
            # print(f"Saved corrected file version 2 to: {output_path_2}")


if __name__ == "__main__":
    input_directory = "inputs"
    output_directory = "output"

    process_files_in_directory(input_directory, output_directory)
