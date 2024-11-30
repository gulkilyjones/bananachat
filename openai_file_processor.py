import openai
import os
import argparse
from pathlib import Path

def process_file(input_file: str, output_file: str, api_key: str, temperature: float) -> None:
    """
    Read content from input file, query OpenAI API, and write response to output file
    
    Args:
        input_file (str): Path to input text file
        output_file (str): Path to output text file
        api_key (str): OpenAI API key
        temperature (float): Temperature setting for response randomness (0.0 to 1.0)
    """
    # Initialize the OpenAI client
    client = openai.OpenAI(api_key=api_key)
    
    # Read input file
    try:
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read().strip()
    except FileNotFoundError:
        print(f"Error: Input file '{input_file}' not found.")
        return
    except Exception as e:
        print(f"Error reading input file: {e}")
        return

    # Send request to OpenAI API
    try:
        response = client.chat.completions.create(
            model="gpt-4-turbo-preview",
            temperature=temperature,
            messages=[
                {
                    "role": "user",
                    "content": content
                }
            ]
        )
        
        response_text = response.choices[0].message.content
        
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return

    # Write response to output file
    try:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(response_text)
        print(f"Response successfully written to {output_file}")
    except Exception as e:
        print(f"Error writing to output file: {e}")
        return

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(
        description='Process text file through OpenAI API',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )
    
    parser.add_argument(
        '-i', '--input',
        default='input.txt',
        help='Path to input text file'
    )
    
    parser.add_argument(
        '-o', '--output',
        default='output.txt',
        help='Path to output text file'
    )

    parser.add_argument(
        '-t', '--temperature',
        type=float,
        default=0.7,
        help='Temperature setting (0.0 to 1.0) - lower values are more deterministic'
    )

    args = parser.parse_args()

    # Validate temperature
    if not 0.0 <= args.temperature <= 1.0:
        print("Error: Temperature must be between 0.0 and 1.0")
        return

    # Get API key from environment variable
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("Error: OPENAI_API_KEY environment variable not set")
        return

    # Process the file with provided arguments
    process_file(args.input, args.output, api_key, args.temperature)

if __name__ == "__main__":
    main()
