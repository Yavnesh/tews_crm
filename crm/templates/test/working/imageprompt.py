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