# Python OCR and File Processing Module
This Python module provides a set of functions designed to process source files within a directory, specifically focusing on extracting ZIP file contents and performing Optical Character Recognition (OCR) on TIFF images. It includes functionality to log actions, handle OCR processing, extract ZIP files into subdirectories, and search text files for specific terms.

## Features

- **ZIP File Extraction**: Extract ZIP files into designated subdirectories.
- **OCR Processing**: Apply OCR to TIFF files, converting images to text.
- **Search Text Files**: Search generated text files for specific terms using boolean operators.
- **Logging**: Setup a logger to record actions and outcomes.

## Requirements

- Python 3.x
- External Libraries:
  - `logging` for logging setup and management.
  - `zipfile` for handling ZIP file extraction.
  - `os` for directory and file path operations.
  - `Pillow (PIL)` for image processing in OCR.
  - `pytesseract` for performing OCR on images.
  - `multiprocessing` for parallel processing of files.

Ensure `pytesseract` and `Pillow` are installed in your environment:

  ```
  pip install Pillow pytesseract
  ```

Additionally, Tesseract OCR software must be installed on your system. Installation instructions vary by operating system.


## Setup

1. Clone or download the module to your local machine.
2. Install the required Python libraries as mentioned in the Requirements section.
3. Ensure Tesseract OCR is correctly installed and accessible from your Python environment.

## Usage

The module provides several functions that can be utilized individually or together to process files within a directory:

### Setup Logger:

Initialize logging for recording the processing activities.

  ```
  logger = setup_logger("your_log_filename.log")
  ```

### Extract ZIP Files:

Call `extract_zip` with the path to a ZIP file and the target extraction directory.

  ```
  extract_zip("path/to/zipfile.zip", "path/to/extraction_directory", logger)
  ```

### Perform OCR on TIFF Files:

Use `ocr_parse` to apply OCR to all TIFF files in a source directory and save the output text files in a target directory.

  ```
  ocr_parse("path/to/source_directory", "path/to/target_directory", logger)
  ```

### Process Source Files:

Automate the extraction of ZIP files and OCR processing of contained TIFF images.

  ```
  process_source_files("path/to/directory_with_zip_files")
  ```

### Search Text Files:

Search for specific terms within the generated text files, supporting boolean operators.

  ```
  search_text_files("path/to/search_directory", "search_string_with_boolean_operators", "output_filename.txt")
  ```

Ensure to replace placeholder paths and filenames with actual values as per your project's directory structure and files.

## Contributing

Contributions to improve the module or add new features are welcome. Please submit pull requests or open issues to discuss proposed changes or report bugs
