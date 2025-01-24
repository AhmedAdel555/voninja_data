import pandas as pd
import pymysql
import uuid  # Import the uuid module
import os  # Import os module to interact with the filesystem

# pip install pandas pymysql openpyxl

# Connect to your database
conn = pymysql.connect(
    host='localhost',
    user='root',
    password='Ahmed2002@#*',
    database='ninja_db'
)
cursor = conn.cursor()

# Directory containing the Excel files
directory_path = 'D:\\voninja_data\data done\Advanced'  # Update with your directory path

# Loop through each file in the directory
for file_name in os.listdir(directory_path):
    print(file_name)
    if True :
        excel_file = os.path.join(directory_path, file_name)

        # Read the sheets into pandas dataframes
        vocab_df = pd.read_excel(excel_file, sheet_name='Sheet1')  # pandas auto-detects engine
        questions_df = pd.read_excel(excel_file, sheet_name='Sheet2')  # pandas auto-detects engine

        # Insert lesson into the lessons table (assuming "1 Greetings.xlsx" is the file name)
        file_name = file_name.replace('.xlsx', '')  # Remove the .xlsx extension

        # Split the file name to extract lesson order and title
        parts = file_name.split(' ', 1)  # Split by the first space
        lesson_order = int(parts[0])  # The first part is the lesson order
        lesson_title = parts[1] if len(parts) > 1 else ''  # The second part is the lesson title

        lesson_id = str(uuid.uuid4())  # Generate a UUID for the lesson
        cursor.execute("INSERT INTO lessons (id, lesson_order, title, level_id) VALUES (%s, %s, %s, %s)",
                      (lesson_id, lesson_order, lesson_title, "22222222-e2a3-471c-8f36-814ec3277f87"))  # level_id = 1 as an example

        # Insert vocabulary data
        for _, row in vocab_df.iterrows():
            word = row['word']
            translated_word = row['translated_word ']
            example = row['statement_example ']
            translated_example = row['translated_statement_example']
            image_url = row['image_url']
            if pd.isna(image_url):
                image_url = None
            vocab_id = str(uuid.uuid4())
            cursor.execute(
                "INSERT INTO vocabulary (id, word, translated_word, statement_example, translated_statement_example, image_url, lesson_id) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s)",  # Corrected the placeholder for image_url
                (vocab_id, word, translated_word, example, translated_example, image_url, lesson_id)
            )        

        # Insert questions and choices
        for _, row in questions_df.iterrows():
            question_content = row['content ']
            correct_answer = row['a']  # Assuming 'a' column contains the correct answer
            choices = [row['a'], row['b'], row['c']]
            
            question_id = str(uuid.uuid4()); # Adjust for your columns

            cursor.execute(
                "INSERT INTO questions (id, content, correct_answer, lesson_id, image_url) "
                "VALUES (%s, %s, %s, %s, %s)",
                (question_id, question_content, correct_answer, lesson_id, row.get('image_url', None))  # Assuming image_url is optional
            )

            # Insert question choices
            for choice in choices:
                cursor.execute(
                    "INSERT INTO question_choices (question_id, choice) VALUES (%s, %s)",
                    (question_id, choice)
                )
    print(file_name)

# Commit the transaction and close the connection
conn.commit()
cursor.close()
conn.close()
