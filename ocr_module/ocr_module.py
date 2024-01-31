import os
import zipfile
from multiprocessing import Pool
from PIL import Image
import pytesseract
import logging

def setup_logger(log_filename):
    """
    Set up a logger to write logs to a file.

    Args:
        log_filename (str): The name of the log file.
    """
    logger = logging.getLogger("unzip_source_files")
    logger.setLevel(logging.INFO)

    # Create a file handler for the log file
    file_handler = logging.FileHandler(log_filename)
    file_handler.setLevel(logging.INFO)

    # Create a formatter
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Add the file handler to the logger
    logger.addHandler(file_handler)

    return logger

def extract_zip(zip_filepath, subdirectory_path, logger):
    """
    Extract the contents of a zip file into a specified subdirectory.

    Args:
        zip_filepath (str): Path to the zip file to be extracted.
        subdirectory_path (str): Path to the subdirectory where the contents will be extracted.
    """
    logger.info(f"Extracting '{zip_filepath}' to '{subdirectory_path}'...")
    with zipfile.ZipFile(zip_filepath, 'r') as zip_ref:
        zip_ref.extractall(subdirectory_path)

def ocr_parse(source_directory, target_directory, logger):
    """
    Perform OCR on all TIFF files in the source directory and save text files in the target directory.

    Args:
        source_directory (str): The directory containing TIFF files to be OCR processed.
        target_directory (str): The directory where the resulting text files will be saved.
        logger (logging.Logger): The logger to use for logging print statements.
    """
    # Create the target directory if it doesn't exist
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Collect the names of existing text files in the target directory
    processed_files = set()
    for filename in os.listdir(target_directory):
        if filename.endswith(".txt"):
            processed_files.add(os.path.splitext(filename)[0])

    # Loop through files in the source directory
    for filename in os.listdir(source_directory):
        if filename.endswith(".tiff") or filename.endswith(".tif"):
            source_path = os.path.join(source_directory, filename)
            target_filename = os.path.splitext(filename)[0] + ".txt"
            target_path = os.path.join(target_directory, target_filename)

            # Check if the base filename (without .txt extension) is already in the set of processed files
            if target_filename[:-4] in processed_files:
                print(f"'{filename}' has already been processed. Skipping...")
                logger.info(f"'{filename}' has already been processed. Skipping...")
                continue

            # Perform OCR on the TIFF file and save the text to the target file
            try:
                image = Image.open(source_path)
                text = pytesseract.image_to_string(image, lang='eng')  # You can specify the language as needed

                with open(target_path, "w", encoding="utf-8") as text_file:
                    text_file.write(text)

                # Add the filename to the set of processed files
                processed_files.add(target_filename)

                print(f"OCR completed for '{filename}'. Text saved to '{target_path}'.")
                logger.info(f"OCR completed for '{filename}'. Text saved to '{target_path}'.")
            except Exception as e:
                print(f"Error processing '{filename}': {str(e)}")
                logger.error(f"Error processing '{filename}': {str(e)}")

def process_source_files(directory):
    """
    Search for .zip files in the specified directory, create subdirectories for each zip file,
    and extract the contents of the zip files into corresponding source directories.

    Args:
        directory (str): The directory to search for .zip files.
    """
    logger = setup_logger("process_source_files.log")

    # List all files in the specified directory
    zip_files = [filename for filename in os.listdir(directory) if filename.endswith(".zip")]

    # Create a pool of worker processes for parallel processing
    with Pool(processes=6) as pool:
        for zip_filename in zip_files:
            zip_filepath = os.path.join(directory, zip_filename)

            # Create a subdirectory based on the zip file name
            subdirectory_name = os.path.splitext(zip_filename)[0]
            subdirectory_path = os.path.join(directory, subdirectory_name, "source")
            target_directory = os.path.join(directory, subdirectory_name, "target")

            if not os.path.exists(subdirectory_path):
                os.makedirs(subdirectory_path)

            # Synchronously extract the zip file's contents
            pool.apply(extract_zip, (zip_filepath, subdirectory_path, logger))

            # Call the ocr_parse function for the extracted files
            pool.apply_async(ocr_parse, (subdirectory_path, target_directory, logger))

            # Log the extraction process
            logger.info(f"Extracting '{zip_filename}' and processing...")

        # Wait for all worker processes to complete
        pool.close()
        pool.join()

def search_text_files(path, search_string, output_filename):
    """
    Search for text files under the specified path containing the search string with boolean operators (AND or OR).
    Generate a list of file paths and write them to the output file.

    Args:
        path (str): The directory path to start the search.
        search_string (str): The search string with boolean operators (e.g., 'foo AND bar' or 'foo OR bar').
        output_filename (str): The name of the output file where the list of matching file paths will be written.
    """
    # Initialize an empty list to store matching file paths
    matching_file_paths = []

    # Split the search string into individual terms
    search_terms = search_string.split()

    # Define a function to check if any search term exists in the file contents
    def check_file_contents(file_contents):
        if 'OR' in search_terms:
            # If 'OR' is present in the search string, check if at least one search term exists
            search_terms.remove('OR')  # Remove 'OR' from the search terms
            return any(term in file_contents for term in search_terms)
        else:
            # If 'OR' is not present, check if all search terms exist
            return all(term in file_contents for term in search_terms)

    # Iterate through files and subdirectories under the specified path
    for root, _, files in os.walk(path):
        for filename in files:
            file_path = os.path.join(root, filename)

            # Check if the file is a text file (you can modify this condition as needed)
            if file_path.endswith(".txt"):
                # print(f"Searching '{file_path}'...")
                with open(file_path, "r", encoding="utf-8") as file:
                    file_contents = file.read()

                    # Check if the search terms satisfy the condition based on 'AND' or 'OR' operator
                    if check_file_contents(file_contents):
                        matching_file_paths.append(file_path)
                        print(f"Match found in '{file_path}'.")

    # Write the list of matching file paths to the output file
    with open(output_filename, "w") as output_file:
        for file_path in matching_file_paths:
            output_file.write(file_path + "\n")
