def read_sales_data(filename):
    """
    Reads sales data from a text file while handling encoding issues.

    Parameters:
        filename (str): Path to the sales data file

    Returns:
        list: List of raw data lines (strings)
    """

    encodings = ['utf-8', 'latin-1', 'cp1252']
    lines = []

    for encoding in encodings:
        try:
            with open(filename, 'r', encoding=encoding) as file:
                raw_lines = file.readlines()

                for line in raw_lines:
                    line = line.strip()

                    # Skip empty lines
                    if not line:
                        continue

                    # Skip header line
                    if line.startswith("TransactionID"):
                        continue

                    lines.append(line)

            # Successfully read file, stop trying encodings
            return lines

        except UnicodeDecodeError:
            # Try next encoding
            continue

        except FileNotFoundError:
            print(f" Error: File '{filename}' not found.")
            return []

        except Exception as e:
            print(" Unexpected error while reading file:", e)
            return []

    # If all encodings fail
    print(" Error: Unable to read file with supported encodings.")
    return []

