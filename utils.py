# utils.py
import wordninja
import pandas
import random
import pandas as pd

# Create an array of related words
related_words = [
    "plot", "scheme", "plan", "blueprint", "diagram", "outline", "strategy",
    "narrative", "storyline", "sequence", "draw", "sketch", "illustrate", "design",
    "render", "doodle", "depict", "trace", "paint", "create", "chart", "graph",
    "visual", "visualize", "representation", "illustration", "infographic", "graphical",
    "map", "cartography", "topography", "layout", "plan", "blueprint", "geography",
    "pie", "slice", "portion", "segment", "circle", "sector", "wedge", "bar", "histogram",
    "column", "vertical bars", "data visualization", "label", "tag", "markers",
    "annotations"
]

# Function to check if a string contains any of the related words
def contains_related_word(input_string):
    for word in related_words:
        if word in input_string.lower():
            return True
    return False

def remove_related_words_from_string(input_string):
    word_list = input_string.split()
    filtered_words = [word for word in word_list if word.lower() not in related_words]
    return ' '.join(filtered_words)

def ensure_pipe_angle_bracket(s):
    # Check if the string ends with >
    if s.endswith('>'):
        # Check if |> is not already present
        if not s.endswith('|>'):
            s = s[:-1] + '|>'
    else:
        # Add |> at the end
        s += '|>'
    return s


def beautify_labels(df):
    """
    Function to beautify column labels using wordninja
    """
    new_columns = []
    for column in df.columns:
        words = wordninja.split(column)
        new_label = ' '.join(word.capitalize() for word in words)
        new_columns.append(new_label)
    df.columns = new_columns


def categorize_columns_by_datatype(data_frame):
    date_columns = []
    int_columns = []
    float_columns = []
    string_columns = []
    
    for column in data_frame.columns:
        dtype = data_frame[column].dtype
        
        if "date" in column.lower() or "/" in column or "-" in column:
            date_columns.append(column)
        elif pd.api.types.is_integer_dtype(dtype):
            int_columns.append(column)
        elif pd.api.types.is_float_dtype(dtype):
            non_missing_values = data_frame[column].dropna()
            is_float = non_missing_values.apply(lambda x: isinstance(x, (float, int)) or (isinstance(x, str) and (x.replace(".", "", 1).replace(",", "", 1).isdigit())))
            if is_float.all():
                float_columns.append(column)
            else:
                string_columns.append(column)
        elif pd.api.types.is_string_dtype(dtype):
            string_columns.append(column)
    
    categorized_columns = {
        "date_columns": date_columns,
        "int_columns": int_columns,
        "float_columns": float_columns,
        "string_columns": string_columns
    }
    
    return categorized_columns


# Function to generate a random prompt
# List of possible chart types
chart_types = [
    "line chart",
    "bar chart",
    "scatter plot",
    "histogram",
    "pie chart",
    "the distribution of",
    "the horizon distribution of",
]

# List of possible formatting options
formatting_options = [
    "color",
    "line",
]

pair_labels = [
    "by",  
    "in accordance with",
    "according to"
]

chart_actions =[
    "Create",
    "Generate",
    "Plot",
    "Develop",
    "Design",
    "Build",
    "Establish",
    "Render",
    "Depict",
    "Produce",
    "Craft",
    "Chart",
    "Illustrate"
]
def generate_prompt(string_columns, float_columns, date_columns, int_columns):
    chart_type = random.choice(chart_types)

    if float_columns:
        x_column = random.choice(float_columns)
    elif int_columns:
        x_column = random.choice(int_columns)
    elif string_columns:
        x_column = random.choice(string_columns)
    elif date_columns:
        x_column = random.choice(date_columns)
    else:
        x_column = None  # Handle the case when all lists are empty

    act = random.choice(chart_actions)
    
    prompt = f"{act} {x_column} in a {chart_type}"

    if random.choice([True, False]):
        pair = random.choice(pair_labels)
        prompt += f"  {pair} "
    
    if random.choice([True, False]):
        y_columns = random.sample(string_columns + date_columns, random.randint(1,1))
        y_labels = ", ".join(y_columns)
        prompt += f" with {y_labels} on the y-axis"
        
    if random.choice([True, False]):
        formatting_option = random.choice(formatting_options)
        prompt += f" and use {formatting_option} formatting"
    
    if random.choice([True]):
        prompt += f" titled {x_column}"
    
    return prompt


def remove_rows_with_high_nulls(df, threshold_percentage=0.8):
    """
    Remove rows with a high percentage of null values from a DataFrame.

    This function removes rows from the DataFrame where more than the specified
    percentage of values are null (NaN), with the option to apply this operation
    only to the initial rows (potentially representing headers).

    Args:
        df (pandas.DataFrame): The DataFrame to process.
        threshold_percentage (float, optional): The threshold percentage of null
            values above which rows will be removed. Default is 0.8 (80%).

    Returns:
        pandas.DataFrame: The DataFrame with rows containing high null values removed,
        and the first non-null row set as the header.
    """
    # Calculate the threshold based on the percentage of columns
    threshold = int(df.shape[1] * threshold_percentage)

    # Remove rows with more than the threshold NaN values from the DataFrame
    df_cleaned = df.dropna(thresh=threshold)

    # Set the first non-null row as the header
    new_header = df_cleaned.iloc[0]
    df_cleaned = df_cleaned[1:]
    df_cleaned.columns = new_header

    return df_cleaned
