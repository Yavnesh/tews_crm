# import re

# # Input string containing survey questions
# survey_input = """
# **Question of survey 1**
# Which team do you think will win the Concacaf Champions Cup final between Columbus Crew and Pachuca?
# A) Columbus Crew
# B) Pachuca
# C) Can't predict
# D) Don't care

# **Question of survey 2**
# Would you like to see Major League Soccer teams perform better in international competitions?
# A) Yes
# B) No
# C) Don't care

# **Question of survey 3**
# Do you believe the Columbus Crew can make a deep run in the 2023 MLS Cup playoffs?
# A) Yes
# B) No
# C) Don't care
# """

# # Regular expression patterns to extract questions and options
# question_pattern = r"\*\*Question of survey \d+\*\*(.*?)\n"
# options_pattern = r"([A-Z]\)) (.*?)\n"

# # Extract questions and options using regular expressions
# questions = re.findall(question_pattern, survey_input, re.DOTALL)
# options = re.findall(options_pattern, survey_input)

# # Print extracted questions and options
# print("Extracted Questions:")
# for i, question in enumerate(questions, start=1):
#     print(f"Survey {i}: {question.strip()}")

# print("\nExtracted Options:")
# for option in options:
#     print(option[0], "-", option[1])

survey_input = """
**Question of survey 1:**
Do you believe that Virgil van Dijk's potential departure from Liverpool would significantly impact Real Madrid's chances of winning the Champions League?
A) Yes, it would significantly increase Real Madrid's chances.
B) Yes, it would slightly increase Real Madrid's chances.
C) No, it would not affect Real Madrid's chances.
D) No, it would slightly decrease Real Madrid's chances.
E) No, it would significantly decrease Real Madrid's chances.

**Question of survey 2:**
Which of the following factors do you believe has contributed most to Real Madrid's recent dominance in La Liga?
A) Superior squad quality
B) Strong leadership from Carlo Ancelotti
C) Lack of competition from other Spanish clubs
D) Favorable refereeing decisions
E) All of the above

**Question of survey 3:**
Do you agree with the author's assessment that Girona's success in La Liga symbolizes a positive shift towards greater competitiveness in the league?
A) Yes, I strongly agree.
B) Yes, I somewhat agree.
C) No, I am neutral.
D) No, I somewhat disagree.
E) No, I strongly disagree.
"""

# Split the survey input into individual questions
questions = survey_input.split("**Question of survey ")[1:]

# Initialize lists to store questions and options
questions_list = []
options_list = []

# Process each question and extract the question and options
for question in questions:
    # Split the question into question text and options
    question_split = question.split("\n")
    question_text = question_split[0].strip()
    options = [option.strip() for option in question_split[1:] if option.strip()]
    
    # Append the question and options to the respective lists
    
    options_list.append(options)
questions_list.append(options_list)

print(options_list)