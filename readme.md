# LaTeX Problem Processor

This project automates the processing and correction of LaTeX documents containing problem sets. It uses OpenAI's GPT-4 model to generate corrected versions of problems and produces two versions of the output for manual review.

## Features

- Processes `.tex` files from an `inputs` directory.
- Generates two corrected versions of each file, saved in an `output` directory.
- Utilizes custom preamble, postamble, and prompt templates for LaTeX formatting.
- Cleans up artifacts such as Markdown code blocks and LaTeX-specific delimiters.
- Modular and extendable design for future enhancements.

## Requirements

- Python 3.7+
- OpenAI Python SDK

## Setup

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd <repository-folder>
   ```

2. **Install dependencies**:
   ```bash
   pip install openai
   ```

3. **Prepare the directories**:
   Ensure the following directory structure:
   ```
   project-root/
   ├── inputs/          # Directory containing .tex files to process
   ├── output/          # Directory for saving processed files
   ├── formating/       # Directory containing preamble.txt, postamble.txt, and prompt.txt
   └── main.py          # Main script
   ```

4. **Add formatting files**:
   Populate the `formating/` directory with:
   - `preamble.txt`: Contains the LaTeX preamble.
   - `postamble.txt`: Contains the LaTeX postamble.
   - `prompt.txt`: Contains the initial text to guide GPT-4.

5. **Set up the API key**:
   Create a `.env` file in the project root directory with the following content:
   ```env
   OPENAI_API_KEY=your_openai_api_key
   ```
   Replace `your_openai_api_key` with your actual OpenAI API key.

## Usage

1. Place `.tex` files in the `inputs` directory.
2. Run the main script:
   ```bash
   python main.py
   ```
3. The processed files will be saved in the `output` directory as:
   - `v1_<filename>.tex`
   - `v2_<filename>.tex`

## Code Structure

### Key Functions

- `load_file(file_path)`: Reads and returns the content of a file.
- `save_file(file_path, content)`: Saves the provided content to a file.
- `split_problems(content, marker)`: Splits LaTeX content into problems using a specified marker.
- `wrap_document(preamble, problems, postamble)`: Wraps problems with the preamble and postamble.
- `load_formatting(directory)`: Loads preamble, postamble, and prompt templates from a directory.
- `correct_problem(problem_text, prompt_start)`: Uses OpenAI GPT-4 to correct a single problem.
- `postprocess_content(content)`: Removes known artifacts (e.g., code block delimiters).
- `process_latex_content(latex_content, preamble, postamble, prompt, marker)`: Processes and corrects problems in a LaTeX file.
- `process_files_in_directory(input_dir, output_dir, marker)`: Processes all `.tex` files in a directory and generates two corrected versions for each file.

### Main Script

The main script initializes directories and processes all `.tex` files in the `inputs` directory. It saves two corrected versions of each file in the `output` directory.

## Example

Given an input file `inputs/example.tex` with the content:
```latex
\documentclass{article}
\begin{document}
MARKPROB
Original Problem 1
MARKPROB
Original Problem 2
\end{document}
```

The script will generate:

1. `output/v1_example.tex`
2. `output/v2_example.tex`

Each file contains the corrected problems wrapped with the preamble and postamble.

## Notes

- Modify `process_files_in_directory` to customize the two output versions (e.g., changing temperature or prompt).
- Ensure that the OpenAI API key is configured in your environment.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

