from loguru import logger
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import re, random
from tews_crm.settings import GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3

def assign_random_api():
    # List of APIs
    apis_list = [GEMINI_API_KEY_1, GEMINI_API_KEY_2, GEMINI_API_KEY_3]
    # Randomly select an api from the list
    selected_api = random.choice(apis_list)
    
    genai.configure(api_key=selected_api)
    model = genai.GenerativeModel('gemini-pro')

    safety_setting={
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
        }
    return model, safety_setting

def generate_image_prompt(merged_content):
    logger.warning("Starting Generate Image Prompt")

    messages = []
    # Generate content for the first prompt
    prompt_one = generate_image_prompt_one(merged_content)
    messages, response = generate_response_chat(prompt_one, messages)
    
    # Generate content for the second prompt
    prompt_two = generate_image_prompt_two()
    messages, response = generate_response_chat(prompt_two, messages)
    
    # Generate content for the third prompt
    prompt_three = generate_image_prompt_three()
    messages, response = generate_response_chat(prompt_three, messages)
    
    # Generate content for the third prompt
    prompt_four = generate_image_prompt_four()
    messages, response = generate_response_chat(prompt_four, messages)
    
    # Extract pre/post content from the last response
    pre_post_content = extract_pre_post_content(response)
    logger.warning("Ending Generate Image Prompt")

    return pre_post_content

def generate_content_info(merged_content):
    logger.warning("Starting Generate Content Info")

    prompt = generate_content_info_one(merged_content)
    response = generate_response_single(prompt)
    
    pre_post_content = extract_pre_post_content(response)
    logger.warning("Ending Generate Content Info")
    
    return pre_post_content

def generate_content_cta(merged_content):
    logger.warning("Starting Generate Content CTA")

    prompt = generate_content_cta_one(merged_content)
    response = generate_response_single(prompt)
    
    pre_post_content = extract_pre_post_content(response)
    
    questions = pre_post_content.split("**Question of survey ")[1:]

    # Initialize lists to store questions and options
    questions_list = []
    options_list = []

    # Process each question and extract the question and options
    for question in questions:
        # Split the question into question text and options
        question_split = question.split("\n")
        options = [option.strip() for option in question_split[1:] if option.strip()]
        
        # Append the question and options to the respective lists
        
        options_list.append(options)
    questions_list = options_list

    logger.warning("Ending Generate Content CTA")
    
    return questions_list

def generate_meta_info(related_topics, related_query, merged_content):
    logger.warning("Starting Generate Meta Info")

    prompt = generate_meta_info_one(merged_content, related_topics, related_query)
    response = generate_response_single(prompt)
    
    pre_post_content = extract_pre_post_content(response)
    logger.warning("Ending Generate Meta Info")
    
    return pre_post_content

def generate_short_content(merged_content):
    logger.warning("Starting Generate Short Content")

    prompt = generate_short_content_one(merged_content)
    response = generate_response_single(prompt)
    
    pre_post_content = extract_pre_post_content(response)
    logger.warning("Ending Generate Short Content")
    
    return pre_post_content

def generate_trend_topics(merged_content, keyword):
    logger.warning("Starting Generate Trend Topics")

    prompt = generate_trend_topics_one(merged_content, keyword)
    response = generate_response_single(prompt)
    
    pre_post_content = extract_pre_post_content(response)
    logger.warning("Ending Generate Trend Topics")
    
    return pre_post_content

def generate_content(topic, short_content, merged_content, related_topics, related_query, category):
    for item in category:
        author_name =  select_author(item)
    messages = []
    # Generate content for the first prompt
    prompt_one = generate_content_prompt_one(short_content[0])
    messages, response = generate_response_chat(prompt_one, messages)
    
    # Generate content for the second prompt
    prompt_two = generate_content_prompt_two(topic, merged_content, related_topics, related_query, category)
    messages, response = generate_response_chat(prompt_two, messages)
    
    # Generate content for the third prompt
    prompt_three = generate_content_prompt_three()
    messages, response = generate_response_chat(prompt_three, messages)
    
    # Extract pre/post content from the last response
    pre_post_content = extract_pre_post_content(response)
    
    return pre_post_content, author_name

def generate_twitter_post(merged_content):
    logger.warning("Starting Generate Twitter_Post")

    prompt = generate_twitter_post_one(merged_content)
    response = generate_response_single(prompt)
     
    pre_post_content = extract_pre_post_content(response)
    logger.warning("Ending Generate Twitter_Post")
    
    return pre_post_content

def generate_response_chat(prompt, messages):
    model, safety_setting = assign_random_api()
    messages.append({'role': 'user', 'parts': [prompt]})
    response = model.generate_content(messages, safety_settings=safety_setting)
    messages.append({'role': 'model', 'parts': [response.text]})
    return messages, response

def generate_response_single(prompt):
    model, safety_setting = assign_random_api()
    response = model.generate_content(prompt, safety_settings=safety_setting)
    return response

def extract_pre_post_content(response):
    if response.candidates:
        try:
            return response.candidates[0].content.parts[0].text
        except (IndexError, AttributeError) as e:
            # Handle unexpected structure or missing attributes in the response
            print(f"Error accessing candidate parts: {e}")
            return ""
    else:
        if hasattr(response, 'prompt_feedback'):
            # Log or handle the prompt feedback to understand why no candidates were returned
            print(f"Prompt feedback: {response.prompt}")

def select_author(category):
    
    if category == "Technology":
        return "tessa@tewsletter.com"
    elif category == "Entertainment":
        return "ethan@tewsletter.com"
    elif category == "Automobile":
        return "alex@tewsletter.com"
    elif category == "Finance":
        return "monica@tewsletter.com"
    elif category == "Health":
        return "hank@tewsletter.com"
    elif category == "Fashion":
        return "fiona@tewsletter.com"
    elif category == "Food":
        return "carlos@tewsletter.com"
    elif category == "Travel":
        return "gabby@tewsletter.com"
    elif category == "Environment":
        return "eva@tewsletter.com"
    elif category == "Sports":
        return "sam@tewsletter.com"
    elif category == "Politics":
        return "pamela@tewsletter.com"
    else:
        return "william@tewsletter.com"

def split_text(text, start_word, end_word):
    # Define the regular expression pattern
    if end_word is not None:
        pattern = re.compile(f'{re.escape(start_word)}(.*?){re.escape(end_word)}', re.DOTALL)
    else:
        pattern = re.compile(f'{re.escape(start_word)}(.*?)$', re.DOTALL)

    # Search for the text between the start and end words
    match = pattern.search(text)
    # print("extracted_text,,,,,,,,,,,,,,,,,,extracted_text")
    if match:
        # Get the text between the start and end words
        extracted_text = match.group(1).strip()
        # print("extracted_text,,,,,,,,,,,,,,,,,",extracted_text)
        if start_word == "Tags":
            items = [item.strip().replace(":", "").replace("*", "").replace("#", "") for item in extracted_text.split(',')]
            tags = []
            for item in items:
                if item:
                    tags.append(item)
            return tags
        elif start_word == "Tweet":
            items = extracted_text.strip().replace(":", "").replace("*", "").replace("-", "")
            return items
        else:
            final_result = []
            text1 = extracted_text.splitlines(False)
            for t in text1:
                if start_word == "Rising Related Queries" or start_word == "Top Related Queries" or start_word == "Rising Related Topics" or start_word == "Top Related Topics":
                    t = t.strip()[3:]
                result = clean_text(t)
                if result != "":
                    # Add non-empty result to the final result
                    final_result.append(result)
            return final_result
    else:
        return None
    
def clean_text(text):
    pattern = r"\b[a-zA-Z0-9_']+\b"  # Updated pattern to capture all word characters
    words = re.finditer(pattern, text)

    # Extract clean words (non-empty)
    clean_words = []
    for word in words:
        clean_word = word.group().strip()
        if clean_word:
            clean_words.append(clean_word)

    # Join cleaned words and add period (optional)
    result = ' '.join(clean_words)
    if text.strip().endswith("."):
        result += "."

    return result


def generate_image_prompt_one(merged_content):
    prompt = """
        {}
        Analyze the above article by taking suggestions from the points given below.
            a) Key Concepts and Entities: Identify the main topics, characters, locations, or objects mentioned in the article.
            b) Visual Style and Setting: Try to understand the overall tone and setting described in the article. Is it a realistic scene, a fantasy world, or something more abstract?
            c) Action and Details: Pay attention to any actions or specific details that would be visually interesting in an image.

        For the above article, think of 5 very simple ideas to describe a scene for image generation.
        Make sure the ideas are very relevant to the content of article, Artice reading Audience is attracted to the scene, loves the image ideas and are compelled to click on that image. 
        The intended purpose is to show these image ideas on cover photo of the article i shared with you.
        The target audience is of US location and the target audience loves to read articles and blog posts and are compelled to open a article by looking at the image.

        Note : The ideas must be very simple to portrait that even a 10 year old can draw the scene.
        Note : Image should not contain any text until it is a proper word in oxford dictonary.
            """.format(merged_content)
    return prompt

def generate_image_prompt_two():
    prompt = """
        Now for the each of these ideas.
            Craft an Image Prompt for each idea by taking suggestions from the points given below.
                a) Start with Core Elements: Include the key concepts and entities you identified. Use descriptive language to convey their characteristics.
                    Example:A photorealistic image of a majestic ancient castle perched on a cliff overlooking a stormy ocean. The castle has tall towers and a long, winding stone bridge leading to its entrance.
                b) Incorporate Details and Style: Refine the prompt based on the style and setting you identified.
                    Example (Adding Details and Style): A high-resolution image of a majestic medieval castle perched on a rocky cliff overlooking a stormy ocean at sunset. The castle has tall, round towers with pointed roofs and a long, moss-covered stone bridge leading to its massive wooden gates. Dark storm clouds gather above, casting dramatic shadows on the castle walls.
                c) Focus on Clarity: Use phrases like "high-resolution," "sharp," or "detailed" to emphasize the desired image quality.
                d) Use References: If the article mentions specific places, objects, or art styles, you can include them in the prompt (e.g., "castle in the style of Hieronymus Bosch").
                e) Action and Emotion: Consider incorporating actions or emotions of characters to make the image more engaging (e.g., "a knight bravely defending the castle gate").
        
            Also, look into these points to hep you to craft a better image prompt.


            Try visually well-defined objects (something with a lot of photos on the internet)

            Try: Wizard, priest, angel, emperor, necromancer, rockstar, city, queen, Zeus, house, temple, farm, car, landscape, mountain, river


            Strong feelings or mystical-sounding themes also work great

            Try: “a sense of awe” “the will to endure”  “cognitive resonance”  “the shores of infinity”
            “the birth of time” “a desire for knowledge” “the notion of self” 



            Try describing a style

            Examples: “a cyberpunk wizard” “a surreal landscape” “a psychedelic astronaut” 

            Try: cyberpunk, psychedelic, surreal, vaporwave, alien, solarpunk, modern, ancient, futuristic, retro, realistic, dreamlike, funk art, abstract, pop art, impressionism, minimalism


            Try invoking unique artists to get a unique style 

            Examples: “Temple by James Gurney” “Father by MC Escher”

            Try: Hiroshi Yoshida, Max Ernst, Paul Signac, Salvador Dali, James Gurney, M.C. Escher, Thomas Kinkade, Ivan Aivazovsky, Italo Calvino, Norman Rockwell, Albert Bierstadt, Giorgio de Chirico, Rene Magritte, Ross Tran, Marc Simonetti, John Harris, Hilma af Klint, George Inness, Pablo Picasso, William Blake, Wassily Kandinsky, Peter Mohrbacher, Greg Rutkowski, Paul Signac, Steven Belledin, Studio Ghibli

            Combine names for new styles: “A temple by Greg Rutkowski and Ross Tran”



            Try invoking a particular medium

            If the style is unspecified, it will lean towards photorealism

            Examples: “a watercolor painting of a landscape” “a child's drawing of a home”

            Try: painting, drawing, sketch, pencil drawing, w, woodblock print, matte painting, child's drawing, charcoal drawing, an ink drawing, oil on canvas, graffiti, watercolor painting, fresco, stone tablet, cave painting, sculpture, work on paper, needlepoint



            Speak in positives. Avoid negatives 

            Language models often ignore negative words (“not” “but” “except” “without”).

            Avoid: “a hat that’s not red” “			Try: “a blue hat”
            Avoid: “a person but half robot” 		Try: “half person half robot”



            Specify what you want clearly

            Avoid: “monkeys doing business”		Try: “three monkeys in business suits”


            If you want a specific composition, say so!

            Examples: “a portrait of a queen” “an ultrawide shot of a queen” 
            Disco Diffusion v5.1 [w/ Turbo] - Colaboratory 
            Try: portrait, headshot, ultrawide shot, extreme closeup, macro shot, an expansive view of

            Too many small details may overwhelm the system:

            Avoid: “a monkey on roller skates juggling razor blades in a hurricane” 
            Try: “a monkey that’s a hurricane of chaos”

            Try taking two well defined concepts and combining them in ways no one has seen before
            f
            Examples: “cyberpunk shinto priest” “psychedelic astronaut crew” “river of dreams” “temple of stars” “queen of time” “necromancer capitalist”

            Try to use singular nouns or specific numbers

            Vague plural words leave a lot to chance (did you mean 2 wizards or 12 wizards?)

            Avoid: “cyberpunk wizards”		Try: “three cyberpunk wizards”
            Avoid: “psychedelic astronauts”	Try: “psychedelic astronaut crew” (implies a crew shot)


            Avoid concepts which involve significant extrapolation 

            Avoid: “an optimistic vision of an augmented reality future” 
            Try: “a solarpunk city filled with holograms”

            Avoid: “Clothes humans will wear 12,000 years into the future”
            Try: “wildly futuristic clothing with glowing and colorful decoration”
            """
    return prompt

def generate_image_prompt_three():
    prompt = """
        Now can you rate and rank these image prompts.
        Target Audience: The target audience is of US location and the target audience loves to read articles and blog posts and are compelled to open a article by looking at the image.
        Style Preference: I have a preferred artistic style Digital art with cartoon and animation representation which looks like real.
            """
    return prompt

def generate_image_prompt_four():
    prompt = """
        Select the top ranked image prompt which can be used. 
        Please refine the prompt to get very clear and professional cover photo.
        Also Make sure that the decription of the prompt is so crystal clear and full of information that it does not generate any image which is distorted or unclear to the audience.
                """
    return prompt

def generate_content_info_one(merged_content):
    prompt = """
          {}
    For the above given blog post 
        1. Provide a category for this blog post which is best fit to any item in the list.
        List - [Technology, Entertainment, Automobile, Finance, Health, Fashion, Food, Travel, Environment, Sports, Politics]  
        If the category does not relate to any item in list then set category as "Other"
        2. Provide a sub category for this blog post
        3. Provide 5 very relavent tags for this blog post
    The output must be in the below given format
        Category : "One Word Category Name"
        Sub Category: "One Word Sub Category Name"
        Tags: "One Word 5 tags in list format"
            """.format(merged_content)
    return prompt

def generate_content_cta_one(merged_content):
    prompt = """
            Article Content: {}

            Prompt:
            Please create 3 survey question related to the article topic.
            Your question should be clear, concise, and relevant to the content discussed in the article.
            Consider asking about readers' opinions, preferences, experiences, or knowledge related to the topic.
            You can also provide multiple-choice options, true/false statements, yes/no questions.
            Dont give options as Other 
            
            Give output in this format:(Follow Strictly)
            **Question of survey 1**
            Question 1
            A) Options A
            B) Options B
            C) Options C
            D) Options D
            E) Options E

            **Question of survey 2**
            Question 2
            A) Options A
            B) Options B
            C) Options C
            D) Options D
            E) Options E

            **Question of survey 3**
            Question 3
            A) Options A
            B) Options B
            C) Options C
            D) Options D
            E) Options E

            Example:
            1. "Based on the article's discussion of sustainable energy solutions, what is your opinion on the most effective renewable energy source for residential use?"
            A) Solar
            B) Wind
            C) Hydroelectric
            D) Geothermal
            E) Other (Please specify)

            2. "After reading about the benefits of remote work in the article, do you believe remote work will become more prevalent in the future?"
            A) Yes
            B) No

            3. "Which statement best describes your opinion on the importance of mental health awareness, as discussed in the article?"
            A) True: Mental health awareness is crucial for overall well-being.
            B) False: Mental health awareness is not a significant concern.

            4. "Are you currently implementing any of the strategies mentioned in the article for improving work-life balance?"
            A) Yes
            B) No

            5. "Do you agree with the article's perspective on the impact of social media on mental health?"
            A) Agree
            B) Disagree
            """.format(merged_content)
    return prompt

def generate_meta_info_one(merged_content,related_topics,related_query):
    prompt = """
            
            Generate compelling meta descriptions for an article page using the following inputs:

            Article Content: {}
            Related Queries: {} Aim to incorporate these queries naturally into the meta descriptions to address potential reader interests.
            Related Topics: {} Use these topics to frame the meta descriptions in a way that resonates with broader themes or discussions surrounding the topic.
            
            Instructions:

            Craft concise and engaging meta descriptions (approximately 150-300 characters) that captivate readers' attention and inspire curiosity.
            Incorporate elements from the article content, related queries, and related topics to provide valuable insights and attract clicks.
            Aim to address potential reader interests, answer questions, and highlight the article's relevance and value.
            Example Inputs:

            Article Content:[Insert article summary or excerpt here]
            Related Queries:[Query 1,Query 2,Query 3,...]
            Related Topics: [Topic 1,Topic 2,Topic 3,...]

            Example Output (Meta Descriptions):

            "Discover the latest insights on [Topic 1] and [Topic 2]. Explore key questions such as [Query 1] and [Query 2] in our comprehensive article."
            "Uncover expert analysis and tips for navigating [Topic 3] trends. Get answers to common questions like [Query 3] and more."
            "Dive into the world of [Topic 1] with our in-depth article. Learn about [Topic 2] and explore related topics, including [Related Topic]."
            
            Give only one output and make sure it is 250 characters.

            """.format(merged_content, related_query, related_topics)
    return prompt
         
def generate_short_content_one(merged_content):
    prompt = """
        {}
            Go through the above content and Create an article for me which i can post on my blog 
        """.format(merged_content)
    return prompt

def generate_trend_topics_one(merged_content, keyword):
    prompt = """
            Input:

            Content: {}
            Keyword: {}

            Number of Outputs:
            40 (10 Rising Related Queries, 10 Rising Related Queries, 10 Rising Related Topics, 10 Top Related Topics)

            Output Categories:

            Rising Related Queries (10): Formulate 50 related queries that are currently experiencing a rise in search volume and are highly relevant to the provided content and keyword. Rank these and pick first 10.

            Top Related Queries (10): Formulate 50 related queries that have consistently high search volume and are highly relevant to the provided content and keyword. Rank these and pick first 10.

            Rising Related Topics (10): Identify 50 related topics that are currently experiencing a rise in interest and are directly connected to the provided content's main theme. Rank these and pick first 10.

            Top Related Topics (10): Identify 50 established, high-volume related topics that directly enhance user understanding of the provided content. Rank these and pick first 10.


            Additional Considerations:

            Prioritize long-tail keywords within the queries when possible.
            Consider incorporating location-specific elements if applicable to the target audience.
            Be mindful of seasonal trends that might influence user search patterns.
            Focus on generating clear, concise, and grammatically correct queries and topics.

            Example:

            Input:

            Content: (Insert your actual content here)
            Keyword: Healthy Eating
            Output: (The model will generate the following based on your content and the keyword)

            Related Queries:

            Rising Related Queries (10): (This section will have 10 examples, like the ones below)
            10 easy healthy meals for busy people 2024
            how to start a healthy eating plan for beginners
            healthy meal prep tips and tricks
            best grocery shopping list for healthy eating
            are there any risks to healthy eating? (if applicable)

            Top Related Queries (10): (This section will have 10 examples, like the ones below)
            benefits of healthy eating
            healthy eating tips to lose weight
            healthy recipes for weight loss
            what is a healthy diet?
            how to eat healthy on a budget

            Related Topics:

            Rising Related Topics (10): (This section will have 10 examples, like the ones below)
            intermittent fasting for weight loss
            the gut microbiome and healthy eating
            plant-based diets for beginners
            healthy meal delivery services
            the impact of processed foods on health

            Top Related Topics (10): (This section will have 10 examples, like the ones below)
            nutrition and healthy eating
            healthy lifestyle habits
            weight management
            chronic disease prevention
            healthy eating for children

        """.format(merged_content, keyword)
    return prompt

def generate_content_prompt_one(short_content):
    prompt = """
    {}
    Analyze the above content  
    Tell me who is the [Target Audience]
    Give me an Outline: [Provide a basic outline with section headings]
        """.format(short_content[0])
    return prompt

def generate_content_prompt_two(topic, merged_content, related_topics, related_query, category):
    prompt = """
    Highly Detailed Prompt for Generative Model Article Writing

        Target Topic: {}
        Content: {}
        Related Topics: {}
        Related Queries: {}
        Target Keywords: [List of relevant keywords, by analyzing Related Topics and Related Queries]
        Writing Style: Mix of Formal, Conversational and Humorous with a {} touch
        Outline: From previous prompt response
        Target Audience : From previous prompt response
        Strict Note - Target Word Count: 1200 Words

        Generate a well-structured and informative article targeting [Target Audience] on the topic of [Your Topic]. Leverage the provided content as a foundation and seamlessly integrate it to address the listed related topics and answer the related queries. Optimize the article for the provided target keywords while maintaining a natural language flow and reader engagement.

        Here are some additional details for the generative model to consider:

        Headline: Craft a creative and attention-grabbing headline that accurately reflects the article's content.
        Introduction: Write a compelling introduction using the chosen writing style to hook the reader and provide a brief overview of the main points.
        Body: Structure Follow the provided outline, ensuring a clear and logical flow between sections.
        Conclusion: Summarize your key points and leave a lasting impression. Consider including a call to action (CTA) in conclusion itself.
        
            """.format(topic,merged_content,related_topics,related_query,category)

    return prompt

def generate_content_prompt_three():
    prompt = """
    For the above generated article do the following 

        1. I can see that the words limit is less than 1000 words. Please add some more content to make it more than 1000 words.

        2. Proofreading: While the model will generate the content, it's recommended to proofread the final article for any grammatical e-rrors or awkward phrasing.

        3. Remove all the credits and authors information from the given content and also, make it look like a work of Human.

        4. If any additional details are there from previous output then if they are relavant then add that to the article in body section

        5. Give me result in 4 parts - heading, intro, body, conclusion.
        Follow this Format
        Heading : the heading goes here 
        Introduction : here goes introduction 
        Body: Here goes body content 
        Conclusion: Here goes conclusion 
            """
    return prompt

def generate_twitter_post_one(merged_content):
    prompt = """
         {}
        For the above provided Content create a tweet for me following the below instructions
        1. Briefly describe the content you want to tweet about. What are the key points or main idea?
        2. Who are you trying to reach with your tweet? Knowing your audience can help tailor the tone and content. (e.g., Developers, Marketing professionals, General audience)
        3. Do you want to ask a question, spark a conversation, or simply share information? This can influence the tone and phrasing of your tweet.
        4. Are there any relevant hashtags you want to include to increase reach? (e.g., #MachineLearning, #ContentMarketing)
        5. Do you want people to learn more, visit a link, or take any specific action?
        6. Tweet must be less than 280 characters otherwise it is not a tweet

        Here's an example for output tweet :
        Tweet : Fascinated by the potential of AI in content creation!  Could it be a game-changer for marketers?   #ContentMarketing #AI
            """.format(merged_content)
    return prompt
