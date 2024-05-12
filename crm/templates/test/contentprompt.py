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

merged_content = """
IPL 2024, LSG vs MI IPL Highlights, Lucknow Super Giants vs Mumbai Indians: Lucknow Super Giants beat Mumbai Indians by four wickets in a low-scoring clash on Tuesday. LSG chased down the 145-run modest target in 19.2 overs thanks to Marcus Stoinis (62 off 45). Nicholas Pooran hit the winning runs for his side when things went a bit haywire for LSG in the death overs. Nehal Wadhera scored 46, while Tim David gave a final push with an unbeaten 32 as Mumbai Indians posted 144/7 in 20 overs against Lucknow Super Giants. Mohsin Khan was the pick of the bowlers with two wickets as LSG bowlers hunt in a pack to put Mumbai on backfoot. Lucknow Super Giants skipper KL Rahul won the toss and elected to bowl first against Mumbai Indians at Ekana Stadium, Lucknow. Mayank Yadav returns in LSG's playing XI, while Quinton de Kock faced the axe to make way for Ashton Turner.
 After back-to-back losses in their ongoing campaign in IPL 2024, Mumbai Indians' chances to make the playoffs this season significantly reduced. And if they lose today at the Ekana Stadium in Lucknow against the KL Rahul-led Lucknow Super Giants, they will find themselves in the same situation as Royal Challengers Bengaluru. When the season had kicked, Mumbai looked one of those teams who were certain to make the playoffs despite their lack of spin options. On paper, they had the best batting and pace unit. Yet, injuries of Jason Behrendorff and Dilshan Madushanka and their replacements - Luke Wood and Kwena Maphaka - having a poor run of form, along with Nuwan Thushara, have left MI in a precarious position. Furthermore, Gerald Coetzee, despite his 12 wickets in eight games, has been rather inconsistent with the ball. Jasprit Bumrah, with 14 wickets at an economy rate of well under seven, has been their only standout bowler.

Lucknow, too, head into the match on the back of a loss in their previous game, yet they are favourites to inflict damage on Mumbai for two reasons - they will be playing at home and have been boosted by the return of Mayank Yadav.

However, amid the IPL 2024 battle in Lucknow and the scenarios for the two teams for the playoffs, the one that will take centrestage will be Rahul. The LSG skipper will have one last shot, probably, to stake claim on the second wicketkeeper's spot in the Indian team before BCCI announces the T20 World Cup squad.

Rahul's strike-rate in the shortest format has always been a bone of contention. Despite the advantage of field restrictions in the Powerplay, Rahul has always been a slow starter in IPL. However, the LSG captain has managed to change gears this season. In the 2024 edition, he scored 378 runs at a strike rate of 144.27 but it is still less than that of Rishabh Pant (160.60) and Sanju Samson (161.08).

While comeback man Pant has all but sealed the first wicketkeeper's spot for the World Cup tournament in the Caribbean islands and the USA in June by displaying some sharp work behind the stumps and sensational knocks with the bat, Samson has also made a strong case for himself by playing match-winning knocks for Rajasthan Royals at a brisk pace.

In such a scenario, Rahul needs to play more fearlessly and exploit the field restrictions not only to strengthen his Indian team selection prospects but also to help his side score in excess of 200 runs, which has become a norm in this edition.
"""

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

**Name:** Sports Savant Sam  
                    **Place:** Sports Central  
                    **Profile:** Play ball! I'm Sports Savant Sam, your MVP for all things sports in the heart of Sports Central. Whether it's touchdowns or home runs, slam dunks or birdies, I've got the play-by-play coverage and in-depth analysis to keep you on the edge of your seat. So grab your jersey and join me for a front-row seat to the thrilling world of athletics!

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

        """

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



"""


    For the above provided Article.
    
    Analyze the Article:
        a) Key Concepts and Entities: Identify the main topics, characters, locations, or objects mentioned in the article.
        b) Visual Style and Setting: Try to understand the overall tone and setting described in the article. Is it a realistic scene, a fantasy world, or something more abstract?
        c) Action and Details: Pay attention to any actions or specific details that would be visually interesting in an image.

    Craft the Image Prompt: 
        a) Start with Core Elements: Include the key concepts and entities you identified. Use descriptive language to convey their characteristics.
            Example:A photorealistic image of a majestic ancient castle perched on a cliff overlooking a stormy ocean. The castle has tall towers and a long, winding stone bridge leading to its entrance.
        b) Incorporate Details and Style: Refine the prompt based on the style and setting you identified.
            Example (Adding Details and Style): A high-resolution image of a majestic medieval castle perched on a rocky cliff overlooking a stormy ocean at sunset. The castle has tall, round towers with pointed roofs and a long, moss-covered stone bridge leading to its massive wooden gates. Dark storm clouds gather above, casting dramatic shadows on the castle walls.
        c) Focus on Clarity: Use phrases like "high-resolution," "sharp," or "detailed" to emphasize the desired image quality.
    
    Additional Tips:

        a) Use References: If the article mentions specific places, objects, or art styles, you can include them in the prompt (e.g., "castle in the style of Hieronymus Bosch").
        b) Action and Emotion: Consider incorporating actions or emotions of characters to make the image more engaging (e.g., "a knight bravely defending the castle gate").
    
        
    Special Note: I need images in a digital cartoon art style
    Create a Animated scene which can be generated using stable diffusion AI model for creating professional digital art.
    




"""