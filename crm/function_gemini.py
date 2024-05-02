import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold


genai.configure(api_key="AIzaSyDUvhzuC5-xrgN1pVXc9knhGlv30sLlw34")
model = genai.GenerativeModel('gemini-pro')

safety_setting={
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

def generate_image_prompt(merged_content):

    prompt_one = """
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

            """.format(merged_content)

    messages = [
        {'role':'user',
        'parts': [prompt_one]}
    ]
    response = model.generate_content(messages, safety_settings = safety_setting)

    print("response.text--prompt one---------", response.text)

    messages.append({'role':'model',
                    'parts':[response.text]})

    prompt_two = """

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

    messages.append({'role':'user',
                    'parts':[prompt_two]})

    response = model.generate_content(messages, safety_settings = safety_setting)

    messages.append({'role':'model',
                    'parts':[response.text]})

    print("response.text--prompt two---------", response.text)

    prompt_three = """

        Now can you rate and rank these image prompts.
        Target Audience: The target audience is of US location and the target audience loves to read articles and blog posts and are compelled to open a article by looking at the image.
        Style Preference: I have a preferred artistic style cartoon and animation.
            """

    messages.append({'role':'user',
                    'parts':[prompt_three]})

    response = model.generate_content(messages, safety_settings = safety_setting)

    messages.append({'role':'model',
                    'parts':[response.text]})

    print("response.text--prompt three---------", response.text)

    prompt_four = """

        Select the top ranked image prompt which can be used. 
        Please refine the prompt to get very clear and professional cover photo.
        Also Make sure that the decription of the prompt is so crystal clear and full of information that it does not generate any image which is distorted or unclear to the audience.
            
            """

    messages.append({'role':'user',
                    'parts':[prompt_four]})

    response = model.generate_content(messages, safety_settings = safety_setting)

    messages.append({'role':'model',
                    'parts':[response.text]})

    print("response.text--prompt four---------", response.text)

    if response.candidates:
        pre_post_content = response.candidates[0].content.parts[0].text
    else:
        pre_post_content = ""

    print("pre_post_content---------------", pre_post_content)
    return pre_post_content

def generate_content_info(merged_content):
    post_prompt = """
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

    prompt_content_response = model.generate_content(post_prompt, safety_settings=safety_setting)
    # print("prompt_content_response------------------------------", prompt_content_response)
    if prompt_content_response.candidates:
        pre_post_content = prompt_content_response.candidates[0].content.parts[0].text
    else:
        pre_post_content = ""
    # print("pre_post_content----------->", pre_post_content)
    
    return pre_post_content

def generate_content(merged_content,category):
    for item in category:
        category = item
    author_profile, author_name =  select_author(category)
    
    prompt_one = """
    {}
    Analyze the above content to make a new blog post! 
    Tell me what all you analysed about the content.
        """.format(merged_content)

    messages = [
        {'role':'user',
        'parts': [prompt_one]}
    ]
    response = model.generate_content(messages, safety_settings = safety_setting)

    print("response.text--prompt one---------", response.text)

    messages.append({'role':'model',
                    'parts':[response.text]})

    prompt_two = """
    {}
    This is an author profile. The author is an expert at writing structured blogs as per his/her personality and charcterstics. The Author uses below format to Structure any blog must be. 1. Craft a Compelling Title/Headline: Introduces the main idea of the article 2. Create an Introduction: Tells the reader what the article will be about 3. Body: Goes in-depth about the topic of the article. Use Transition Words 4. Conclusion: Wraps up the main ideas. Author has given an example also about how to structure a blog post. Example Heading : the heading goes here Introduction : here goes introduction Body: Here goes body content Conclusion: Here goes conclusion 

    The Author uses below format to Structure any blog must be. 
            1. Craft a Compelling Title/Headline: Introduces the main idea of the article
            2. Create an Introduction: Tells the reader what the article will be about
            3. Body: Goes in-depth about the topic of the article. Use Transition Words
            4. Conclusion: Wraps up the main ideas.
        Author has given an example also about how to structure a blog post.
        Example
            Heading : the heading goes here
            Introduction : here goes introduction 
            Body: Here goes body content
            Conclusion: Here goes conclusion 

    Here are some additional points that could be included in the profile, depending on the author's preferences:

    Writing style: Is the author known for a specific writing style, such as informative, humorous, or conversational?
    Target audience: Who are the author's ideal readers?
    Topics of expertise: Does the author have specific areas of knowledge they write about most often?
    Call to action: Does the author typically include a call to action in their blog posts, such as encouraging readers to subscribe or share their content?

            """.format(author_profile)

    messages.append({'role':'user',
                    'parts':[prompt_two]})

    response = model.generate_content(messages, safety_settings = safety_setting)

    messages.append({'role':'model',
                    'parts':[response.text]})

    print("response.text--prompt two---------", response.text)

    prompt_three = """

        Now you have the analysis of the content and the author information.
        Understand the below text and write this content as the Author as per the struture and author profile given.
        Change the words completely around, make it as it's very different and not the same.
        Remove all the credits and authors information from the given content and also, arrange the the content in a way that it does not look like a work of AI.
        Also, add some more depth and make it fun as it is going on my blog.
        Give me result in 4 parts - heading, intro, body, conclusion.
        Keep in mind the content should comply with the safety guidelines of the generative model 
        Follow Strictly : More than 1000 words
            """

    messages.append({'role':'user',
                    'parts':[prompt_three]})

    response = model.generate_content(messages, safety_settings = safety_setting)

    messages.append({'role':'model',
                    'parts':[response.text]})

    print("response.text--prompt three---------", response.text)

    prompt_four = """

        I can see that the words limit is less than 1000 words. Please add some more content to make it more than 1000 words.
            """

    messages.append({'role':'user',
                    'parts':[prompt_four]})

    response = model.generate_content(messages, safety_settings = safety_setting)

    messages.append({'role':'model',
                    'parts':[response.text]})

    print("response.text--prompt four---------", response.text)

    if response.candidates:
        pre_post_content = response.candidates[0].content.parts[0].text
    else:
        pre_post_content = ""

    print("pre_post_content---------------", pre_post_content)

    return pre_post_content, author_name

def select_author(category):
    if category == "Technology":
        author = """**Name:** Tech Titan Tessa  
                    **Place:** Silicon Valley  
                    **Profile:** Hey there, I'm Tech Titan Tessa, your go-to guru for all things tech! Hailing from the innovation hub of Silicon Valley, I've got my finger on the pulse of the latest gadgets, gizmos, and breakthroughs in the world of technology. Whether it's dissecting the newest smartphone release or diving deep into the realms of artificial intelligence, I'm here to decode the digital landscape and keep you ahead of the curve.
                """
        return author, "Tessa"
    elif category == "Entertainment":
        author = """**Name:** Entertainment Extraordinaire Ethan  
                    **Place:** Hollywood  
                    **Profile:** Lights, camera, action! I'm Ethan, your Entertainment Extraordinaire straight from the heart of Hollywood. With exclusive access to the glitz and glamour of the entertainment industry, I've got the inside scoop on all your favorite celebrities, movies, and TV shows. From red carpet premieres to behind-the-scenes drama, join me for a front-row seat to the world of entertainment!
                """
        return author, "Ethan"
    elif category == "Automobile":
        author = """**Name:** Auto Aficionado Alex  
                    **Place:** Detroit  
                    **Profile:** Vroom vroom, it's Auto Aficionado Alex here, revving up from the Motor City! As a connoisseur of all things automotive, I'm here to steer you through the fast-paced world of cars, trucks, and everything on wheels. From the latest models to cutting-edge technology, buckle up and join me for a thrilling ride down the highway of automotive news!
                """
        return author, "Alex"
    elif category == "Finance":
        author = """**Name:** Financial Whiz Monica  
                    **Place:** Wall Street  
                    **Profile:** Welcome to the financial frontier with yours truly, Financial Whiz Monica, reporting live from Wall Street! With a keen eye for market trends and a knack for navigating the complexities of finance, I'm here to guide you through the ever-changing landscape of money matters. From stock market fluctuations to personal finance tips, let's make sense of the numbers together!
                """
        return author, "Monica"
    elif category == "Health":
        author = """**Name:** Health Maven Hank  
                    **Place:** Health Hub  
                    **Profile:** Hey there, I'm Health Maven Hank, your trusted source for all things wellness! Nestled in the heart of the Health Hub, I've got the latest scoop on fitness trends, medical breakthroughs, and everything in between. Whether you're looking to boost your immune system or stay in tip-top shape, join me on a journey to optimal health and vitality!
                """
        return author, "Hank"
    elif category == "Fashion":
        author = """**Name:** Fashionista Fiona  
                    **Place:** Fashion Capital  
                    **Profile:** Strike a pose, darlings! It's Fashionista Fiona here, bringing you the hottest trends from the fashion capital of the world. With a flair for style and an eye for couture, I'm your ultimate guide to the runway, the red carpet, and beyond. From haute couture to street style chic, let's explore the ever-evolving world of fashion together!
                """
        return author, "Fiona"
    elif category == "Food":
        author = """**Name:** Culinary Connoisseur Carlos  
                    **Place:** Foodie Haven  
                    **Profile:** Buen provecho, amigos! I'm Culinary Connoisseur Carlos, your taste bud tour guide through the flavorful world of food. From mouth-watering recipes to culinary adventures from around the globe, join me as we savor the sights, smells, and tastes of gastronomic delight. Whether you're a seasoned chef or a kitchen newbie, let's spice things up together!
                """
        return author, "Carlos"
    elif category == "Travel":
        author = """**Name:** Travel Guru Gabby  
                    **Place:** Wanderlust World  
                    **Profile:** Bon voyage, fellow explorers! I'm Travel Guru Gabby, your passport to adventure in the wanderlust world. With a thirst for discovery and a love for new horizons, I'm here to whisk you away on unforgettable journeys to far-flung destinations. From hidden gems to bucket-list must-sees, pack your bags and join me for a whirlwind tour of the globe!
                """
        return author, "Gabby"
    elif category == "Environment":
        author = """**Name:** Environmental Advocate Eva  
                    **Place:** Eco Oasis  
                    **Profile:** Hello, eco-warriors! I'm Environmental Advocate Eva, your voice for planet Earth in the green oasis. With a passion for sustainability and a dedication to preserving our precious natural resources, I'm here to shed light on environmental issues and inspire positive change. From eco-friendly innovations to conservation efforts, let's join forces to protect our planet for future generations!
                """
        return author, "Eva"
    elif category == "Sports":
        author = """**Name:** Sports Savant Sam  
                    **Place:** Sports Central  
                    **Profile:** Play ball! I'm Sports Savant Sam, your MVP for all things sports in the heart of Sports Central. Whether it's touchdowns or home runs, slam dunks or birdies, I've got the play-by-play coverage and in-depth analysis to keep you on the edge of your seat. So grab your jersey and join me for a front-row seat to the thrilling world of athletics!
                """
        return author, "Sam"
    elif category == "Politics":
        author = """**Name:** Political Pundit Pamela  
                    **Place:** Washington D.C.  
                    **Profile:** As a seasoned political analyst based in the heart of the nation's capital, I bring you the latest insights and commentary on the ever-changing landscape of American politics. From Capitol Hill to the campaign trail, join me as we navigate the complexities of government, elections, and policy-making.
                """
        return author, "Pamela"
    else:
        author = """**Name:** Worldly Wanderer William  
                    **Place:** Anywhere and Everywhere  
                    **Profile:** Exploring the wonders of the world, one adventure at a time. From remote villages to bustling metropolises, join me on a journey of discovery and cultural immersion. Let's uncover hidden gems, experience diverse cuisines, and embrace the beauty of our planet.
                """
        return author, "William"


