import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold
import re

genai.configure(api_key="AIzaSyBJaCAFmsYpMcO7OTNEJV6I-Ci9O7-X03Q")
model = genai.GenerativeModel('gemini-pro')

safety_setting={
    HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
    HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }

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
                print("t", t)
                result =clean_text(t)
                print("resu", result)
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
keyword = "Monterrey vs. Columbus"
content = """['The Columbus Crew stun Monterrey on the road in Mexico - MLS side thump Rayados to advance to CONCACAF Champions Cup final vs Pachuca', "What channel is Columbus Crew's second leg match on? Here's how to watch Crew-CF Monterrey", 'Columbus Crew 3-1 Monterrey (May 1, 2024) Game Analysis', 'Monterrey v Columbus Crew | Highlights', 'Monterrey vs. Columbus CONCACAF Champions Cup Highlights | FOX Soccer', 'History! Columbus Crew topple Monterrey to reach Champions Cup final', 'Crew advance to Concacaf Champions Cup Final with 3-1 win over CF Monterrey', 'Columbus Crew down CF Monterrey to lock up spot in CONCACAF Champions Cup Final', 'History! Columbus Crew topple Monterrey to reach Champions Cup final', 'Monterrey vs. Columbus Crew live stream: How to watch Concacaf Champions Cup online, TV channel, odds']
['The Columbus Crew stun Monterrey on the road in Mexico - MLS side thump Rayados to advance to CONCACAF Champions Cup final vs Pachuca Columbus CrewCONCACAF Champions CupMonterrey vs Columbus CrewMonterrey\n\nThe Columbus Crew pulled off a remarkable result against Monterrey in the second leg of their Champions Cup tie to book a place in the final.', "The Crew are back in Mexico for a chance to make more club history in the CONCACAF Champions Cup.\n\nIf Columbus defeats CF Monterrey in the Champions Cup semifinals, the club will advance to the tournament's finals for the first time in history. The Crew have already made it further than they've even been in Champions Cup play, making their first semifinals appearance following a quarterfinal victory over Tigres 4-3 in penalty kicks during the second leg.\n\nThe Crew are going into the second leg against Monterrey with a 2-1 aggregate advantage. Columbus picked up two goals in the first leg at Lower.com Field on April 24 behind the efforts of Cucho Hernandez and Jacen Russell-Rowe.\n\nIn order to advance to the Champions Cup final matchup in regulation, the Crew must finish the second leg with a win, draw or a one-goal loss in which they score at least two goals. Monterrey advances automatically if it records a two-plus goal victory or a victory in which Columbus fails to score.\n\nAccording to CONCACAF guidelines, the first tiebreaker in a series is road goals. The only way the Crew-Monterrey second leg match goes into extra time with a possibility for penalty kicks is if regulation ends and Monterrey holds a 2-1 advantage in the match.\n\nTakeaways from first leg:Columbus Crew take crucial 2-1 advantage over CF Monterrey in Champions Cup\n\nHere's how you can watch the Crew vs Monterrey in their second leg matchup:\n\nWhat time does Columbus Crew play CF Monterrey?\n\nKickoff is set for 10:15 p.m. at Estadio BX in Monterrey, Mexico.\n\nWhat channel is Columbus Crew vs. CF Monterrey?\n\nThe match will be on FS1. Streaming is available via the Fox Sports app. The Spanish broadcast will be on TUDN.\n\nWho is calling Columbus Crew vs. CF Monterrey on FS1?\n\nFox Sports' lead soccer broadcast team of John Strong (play-by-play) and Stu Holden (analyst) will be on the call for the second leg of the Crew-Monterrey Champions Cup semifinal series.\n\nThe duo of Strong and Holden called the first leg matchup between Columbus and Monterrey, as well as the Club America-CF Pachuca semifinal matches.\n\nHow can I to listen to Columbus Crew vs. CF Monterrey on the radio?\n\nThe broadcast of the match will be available on 105.7 FM. Chris Doran will be on the radio call. The Spanish radio broadcast will be available via 102.5 FM La Grande.\n\nColumbus Crew vs CF Monterrey watch party: Is there a watch party for the second leg match?\n\nThe Crew are hosting a watch party at Chase Plaza and the Condado Tacos at Lower.com Field for free at Lower.com Field starting at 9:15 p.m. Though the event is free, tickets are still required, which are available here.\n\nWill Columbus Crew host the Champions Cup final if they advance?\n\nIf the Crew do advance to the final, it is impossible for the match to be hosted in Columbus following the result of the CF Pachuca-Club America match on Tuesday.\n\nPachuca recorded the victory to advance to the final and now has 14 points in Champions Cup play. The Crew have only nine points with the max amount that could be earn tonight being three, putting them below Pachua in the rankings, which determines the host for the final.\n\nbmackay@dispatch.com\n\n@brimackay15\n\nGet more Columbus Crew content by listening to our podcast", "Goals from Aidan Morris and Diego Rossi on either side of halftime led the Columbus to a 3-1 victory over Rayados on Wednesday in Monterrey, Mexico, giving the Crew a 5-2 aggregate win in the Concacaf Champions Cup semifinals.\n\nColumbus, the reigning MLS Cup champion, opened the semifinal series with a 2-1 home victory on April 24.\n\n- Stream on ESPN+: LaLiga, Bundesliga, more (U.S.)\n\nThe Crew advance to oppose another Mexican team, Pachuca, in the final on June 2. Pachuca beat Liga MX rival América 2-1 on Tuesday to cap a 3-2 semifinal victory.\n\nMonterrey leveled the series with an 11th-minute own goal from Crew defender Yevhen Cheberko.\n\nWith seconds left in the first half, Monterrey goalie Esteban Andrada rolled the ball out beyond the 18-yard box but left it short of his intended target. Morris ran onto the ball, drove to the top of the box and rolled a right-footed shot past Andrada, who was stranded at the penalty spot.\n\nColumbus' Alexandru Matan entered the game as a second-half substitute and made an immediate impact. His perfect pass slipped in to Rossi for a 14-yard, left-footed shot that padded the Crew's aggregate advantage.\n\nJacen Russell-Rowe capped Columbus' victory with a counterattack goal in the 89th minute, breaking in alone and chipping the ball past Andrada, who came out to challenge him.\n\nAndrada subsequently saved a penalty kick from Christian Ramírez in second-half stoppage time.\n\nColumbus is headed to the final of the competition, formerly known as the Concacaf Champions League, for the first time. Pachuca is a five-time winner of the event.", '', 'my favs\n\nDISMISS\n\nAccess and manage your favorites here', "The Columbus Crew are on the verge of Concacaf Champions Cup history, storming past Liga MX powerhouse CF Monterrey on Wednesday evening with a 3-1 away victory to take their semifinal series 5-2 on aggregate.\n\nColumbus, who won the opening leg 2-1 at Lower.com Field last week, will visit Pachuca for the June 1 final – looking to join the 2022 Seattle Sounders as Major League Soccer’s only Champions Cup winners.\n\nIf head coach Wilfried Nancy’s team lifts the CCC trophy next month, they’d secure a spot in the 2025 FIFA Club World Cup and 2024 FIFA Intercontinental Cup, plus get regional bragging rights and prize money.\n\nYet Monterrey struck first at Estadio BBVA, courtesy of a Yevhen Cheberko own goal (11') after Maxi Meza's chip over onrushing Crew goalkeeper Patrick Schulte caromed off the crossbar and in off the Ukrainian defender. But Columbus leveled on the final kick of the first half when Aidan Morris (45+4') picked off a restart by Monterrey goalkeeper Esteban Andrada and fired home the Crew’s first of three away goals.", "This is the first time the club has advanced to the Concacaf Champions Cup final in franchise history.\n\nGUADALUPE, Nuevo Leon — The Columbus Crew are advancing to the Concacaf Champions Cup Final after defeating CF Monterrey 3-1 Wednesday night.\n\nColumbus got off to a tough start after Crew defender Yevhen Cheberko scored on his own goal, giving Monterrey a 1-0 advantage in the 11th minute.\n\nIt was quiet on the scoring front for more than 30 minutes, but with just seconds left in the half, Crew midfielder Aidan Morris scored with a shot from outside the box to the bottom left corner to tie the match 1-1.\n\nCrew Forward Diego Rossi netted the Black & Gold’s second goal of the match. He posted his third goal of the tournament and is now only one shy of the Crew’s highest career goal in Concacaf Champions Cut since 2008-09.\n\nThe Crew’s Jacen Russell-Row capped the Crew’s scoring in the 89th minute. He scored in both matches against CF Monterrey, the game-winner on a header in Leg 1 and a second to seal the outright victory.\n\nThe Crew defeated CF Monterrey 2-1 in the first leg of the semifinals on April 24 at Lower.com Field.\n\nThe Black and Gold will now take on CF Pachuca in the final on June 2.\n\nThis is the first time the club has advanced to the Concacaf Champions Cup final in franchise history.\n\nColumbus returns to regular season play on May 11 against rivals FC Cincinnati at Lower.com Field.\n\n📺 10TV+ is available for free: Stay up to date on what's happening in your community with a 24/7 live stream and on demand content from 10TV — available on Roku, Amazon Fire TV and Apple TV.", 'The Columbus Crew traveled to Monterrey and again walked out with a win. The Black & Gold muted Estadio BBVA with a spectacular performance and booked a ticket to the CONCACAF Champions Cup Final after smashing Rayados 3-1 (5-2 on aggregate) at their home Wednesday evening.\n\nThe Crew enjoyed an electric start and found some spaces to test Rayados’ goalkeeper Esteban Andrada.\n\nForward Cucho Hernandez had a long-distance shot in the first minute that went slightly wide.\n\nHowever, things turned tough when unexpectedly Rayados hit first in the 10th minute. Midfielder Maxi Meza controlled a long pass and put it over Crew’s goalkeeper Patrick Schulte. His shot came off the crossbar, but defender Yevhen Cheberko couldn’t slow his pace and tallied an own goal to give the hosts an early lead.\n\nDespite the situation, the MLS champions kept composure and possession of the ball for the next few minutes but could not find open spaces and hurt Rayados.\n\nIn the 19th minute, a late run by midfielder Luis Romo into the box almost extended the Monterrey lead, but the header went just above the crossbar.\n\nBy that time of the game, Rayados’ pressure forced Crew to go back deep in the field and turn over the ball.\n\nFollowing a long time with little to no action, Andrada’s huge mistake opened a window for the Crew.\n\nIn the fourth minute of added time in the first half, after catching a crossed ball, Andrada succumbed to the crowd’s pressure and gave the ball to the wrong teammate.\n\nMorris was paying more attention than anyone else on the field and quickly won the challenge to get possession of the ball and score the equalizer before going to halftime.\n\nThe crowd was not even back to their seats when the Black & Gold scored the second goal. Forward Diego Rossi collected a pass from Alex Matan and slotted the ball to the right of the diving goalkeeper to increase the lead. Rayados desperately looked for a quick response but never couldn’t mount an answer to the knockout blow.\n\nIn the 61st minute, following a bad deflection by Schulte from a crossed ball, defender Gerardo Arteaga caught the rebound, but his shot hit the outside of the net.\n\nAfter the second goal, Crew played out from the back, burned time and made it a point to slow down the game.\n\nAfter a series of wrong deflections and unfortunate rebounds for the Crew, Rayados almost had the equalizer in the 67th minute, but defender Yaw Yeboah stopped the ball on the goal line.\n\nFor the rest of the game, Rayados tried several times with crossed balls, but all the headers ended up in Schulte’s hands, who saved the Crew on multiple occasions without conceding a rebound.\n\nForward German Berterame had his chance in the 70th minute and Brandon Vazquez had his header one minute later, but neither was successful.\n\nWhen the game was almost over, midfielder Derrick Jones, who was subbed in by Aidan Morris minutes earlier, recovered a key ball in the middle. He found Matan who moved the ball on to a fresh Russell-Rowe for the final goal of the match.\n\nChristian Ramirez was fouled in the last moments of play by Andrada, and after a quick VAR review, a penalty kick was called.\n\nAndrada guessed Ramirez’s shot and saved the attempt as the final whistle blew.\n\nColumbus Crew took on two of the most important teams in Mexico and made their way to the CONCACAF Champions final. The team heads back to Columbus to prepare for a clash against FC Cincinnati on May 11th.', "The Columbus Crew are on the verge of Concacaf Champions Cup history, storming past Liga MX powerhouse CF Monterrey on Wednesday evening with a 3-1 away victory to take their semifinal series 5-2 on aggregate.\n\nColumbus, who won the opening leg 2-1 at Lower.com Field last week, will face Pachuca in the June final – looking to join the 2022 Seattle Sounders as Major League Soccer’s only Champions Cup winners.\n\nIf head coach Wilfried Nancy’s team lifts the CCC trophy next month, they’d secure a spot in the 2025 FIFA Club World Cup and 2024 FIFA Intercontinental Cup, plus get regional bragging rights and prize money.\n\nYet Monterrey struck first at Estadio BBVA, courtesy of a Yevhen Cheberko own goal (11') after Maxi Meza's chip over onrushing Crew goalkeeper Patrick Schulte caromed off the crossbar and in off the Ukrainian defender. But Columbus leveled on the final kick of the first half when Aidan Morris (45+4') picked off a restart by Monterrey goalkeeper Esteban Andrada and fired home the Crew’s first of three away goals.\n\nDiego Rossi (49') put the Crew ahead on the night, and 4-2 on aggregate, with a tidy finish after being slipped through by second-half substitute Alex Matan. Then Jacen Russell-Rowe (89') put the finishing touches on the win with a breakaway finish, sending the 2023 MLS Cup champions past the five-time CCC winners and into their first-ever CCC final.\n\nGoals\n\n11’ - MTY - Yevhen Cheberko (OG) | WATCH\n\n45+4' - CLB - Aidan Morris | WATCH\n\n49' - CLB - Diego Rossi | WATCH\n\n89' - CLB - Jacen Russell-Rowe | WATCH\n\nThree Things", 'The Columbus Crew continue their quest to become the second MLS team in as many years to reach the final of the Concacaf Champions Cup on Wednesday, when they travel to Monterrey for the second leg of the semifinals.\n\nThe reigning MLS Cup champions won the first leg 2-1, but the narrow margin means they have it all to play for against one of the competition\'s most acclaimed sides -- Monterrey have won the title five times, most recently in 2021.\n\nHere\'s what you need to know before tuning in.\n\nGolazo Starting XI Newsletter Get your Soccer Fix from Around the Globe Your ultimate guide to the Beautiful Game as our experts take you beyond the pitch and around the globe with news that matters. I agree to receive the "Golazo Starting XI Newsletter" and marketing communications, updates, special offers (including partner offers), and other information from CBS Sports and the Paramount family of companies. By pressing sign up, I confirm that I have read and agree to the Terms of Use and acknowledge Paramount\'s Privacy Policy See All Newsletters Please check the opt-in box to acknowledge that you would like to subscribe. Thanks for signing up! Keep an eye on your inbox. Sorry! There was an error processing your subscription.\n\nHow to watch and odds\n\nDate: Wednesday, May 1 | Time: 10:15 p.m. ET\n\nWednesday, May 1 | 10:15 p.m. ET Location: Estadio BBVA -- Guadalupe, Mexico\n\nEstadio BBVA -- Guadalupe, Mexico TV: FS1 | Live stream: Fubo (try for free)\n\nFS1 | Fubo (try for free) Odds: Monterrey -170; Draw +330; Columbus Crew +450\n\nHow they got here\n\nMonterrey: Things have been fairly straightforward for Monterrey in this edition of the Champions Cup. They beat Guatemala\'s Comunicaciones 7-1 in round one and then two MLS sides before meeting the Crew -- a 3-1 win over FC Cincinnati in the round of 16 and a 5-2 win over Inter Miami in the quarterfinals. American forward Brandon Vazquez has been their top goalscorer in the competition with four goals, including one in the second leg against Miami. They played a fairly even match against the Crew at Lower.com Field last week despite coming out with a one-goal disadvantage, which could be encouraging on home turf.\n\nColumbus Crew: The Crew have already made their deepest-ever run in the competition but no doubt have their sights set on going at least one step further -- and perhaps going all the way. Things have been much tighter for them than it has for Monterrey, though, partially due to the fact that the Champions Cup kicked off just as the MLS season did. They beat the Houston Dynamo 2-1 in the round of 16 before advancing on penalties against Tigres in the quarterfinals, and again face another closely contested matchup on Wednesday. The first leg against Monterrey ultimately favored them -- they out-possessed, outshot and out-passed the opposition -- but the big question for them is if they can do so again away from home.\n\nPrediction\n\nBoth teams enter the matchup in somewhat inconsistent form but expect another competitive matchup that could swing either way. Monterrey likely have the edge because of the home field advantage, but this one could require extra time to settle the score. Pick: Monterrey 2, Columbus Crew 0 (after extra time)']
"""


post_prompt = """
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

        """.format(content,keyword)


prompt_content_response = model.generate_content(post_prompt, safety_settings=safety_setting)

if prompt_content_response.candidates:
    pre_post_content = prompt_content_response.candidates[0].content.parts[0].text
else:
    pre_post_content = ""
print("pre_post_content---------------", pre_post_content)

cleaned_heading = []
cleaned_subheading = []
cleaned_content = []
cleaned_conclusion = []
cleaned_heading = split_text(pre_post_content, "Rising Related Queries", "Top Related Queries")
cleaned_subheading = split_text(pre_post_content, "Top Related Queries", "Rising Related Topics")
cleaned_content = split_text(pre_post_content, "Rising Related Topics", "Top Related Topics")
cleaned_conclusion = split_text(pre_post_content, "Top Related Topics", None)

print("cleaned_heading",cleaned_heading)
print("cleaned_subheading",cleaned_subheading)
print("cleaned_content",cleaned_content)
print("cleaned_conclusion",cleaned_conclusion)


# import re

# def extract_related_queries_topics(text):
#   """
#   Extracts rising and top related queries and topics from a given text.

#   Args:
#       text: The input text containing related queries and topics.

#   Returns:
#       Four lists: rising_queries, top_queries, rising_topics, and top_topics.
#   """

#   rising_queries = []
#   top_queries = []
#   rising_topics = []
#   top_topics = []

#   # Extract sections using headers
#   sections = re.split(r"(Rising|Top) Related (Queries|Topics):", text)

#   # Skip the first empty section
#   sections = sections[1:]

#   # Loop through sections in pairs (header and content)
#   for i in range(0, len(sections), 2):
#     header = sections[i]
#     content = sections[i+1]

#     # Extract list items
#     items = content.strip().split("\n")

#     # Remove leading numbers and extra whitespace
#     items = [item.strip()[2:] for item in items]

#     # Add items to appropriate list based on header
#     if header.startswith("Rising Related Queries"):
#       rising_queries = items
#     elif header.startswith("Top Related Queries"):
#       top_queries = items
#     elif header.startswith("Rising Related Topics"):
#       rising_topics = items
#     elif header.startswith("Top Related Topics"):
#       top_topics = items

#   return rising_queries, top_queries, rising_topics, top_topics

# # Example usage
# text = """
# **Rising Related Queries:**

# 1. Columbus Crew rematch with Pachuca
# 2. Columbus Crew away goals
# 3. Monterrey vs. Columbus Crew betting odds
# 4. How to watch Columbus Crew vs. Monterrey
# 5. Who is calling Columbus Crew vs. Monterrey on FS1?
# 6. Columbus Crew vs. Monterrey broadcast time
# 7. Monterrey vs. Columbus Crew highlights
# 8. Columbus Crew vs. Monterrey game analysis
# 9. Monterrey vs. Columbus Crew history
# 10. Columbus Crew vs. Monterrey tickets

# **Top Related Queries:**

# 1. Columbus Crew vs. Monterrey
# 2. Monterrey vs. Columbus Crew
# 3. Columbus Crew Champions Cup
# 4. Monterrey Champions Cup
# 5. Concacaf Champions Cup
# 6. Columbus Crew soccer
# 7. Monterrey soccer
# 8. Columbus Crew schedule
# 9. Monterrey schedule
# 10. Columbus Crew results

# **Rising Related Topics:**

# 1. Columbus Crew in the Concacaf Champions Cup
# 2. Monterrey in the Concacaf Champions Cup
# 3. The history of the Concacaf Champions Cup
# 4. The format of the Concacaf Champions Cup
# 5. The teams in the Concacaf Champions Cup
# 6. The players in the Concacaf Champions Cup
# 7. The stadiums in the Concacaf Champions Cup
# 8. The fans in the Concacaf Champions Cup
# 9. The media coverage of the Concacaf Champions Cup
# 10. The impact of the Concacaf Champions Cup

# **Top Related Topics:**

# 1. Soccer in the United States
# 2. Soccer in Mexico
# 3. The history of soccer in North America
# 4. The future of soccer in North America
# 5. The role of the Concacaf Champions Cup in the development of soccer in North America
# 6. The impact of the Concacaf Champions Cup on the global soccer landscape
# 7. The economic impact of the Concacaf Champions Cup
# 8. The social impact of the Concacaf Champions Cup
# 9. The cultural impact of the Concacaf Champions Cup
# 10. The legacy of the Concacaf Champions Cup
# """

# rising_queries, top_queries, rising_topics, top_topics = extract_related_queries_topics(text)

# print("Rising Related Queries:", rising_queries)
# print("Top Related Queries:", top_queries)
# print("Rising Related Topics:", rising_topics)
# print("Top Related Topics:", top_topics)
