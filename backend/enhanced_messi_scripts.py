"""
Enhanced Messi Story Scripts - Cinematic Documentary Style
More dramatic, engaging, and emotionally compelling
"""

ENHANCED_SCRIPTS = {
    "messi_getafe_2007": {
        "title": "The Goal That Changed Everything",
        "subtitle": "Messi vs Getafe, 2007",
        "chapters": [
            {
                "title": "The Setup",
                "narration": "April 18th, 2007. Camp Nou holds its breath. A 19-year-old Argentine receives the ball near the halfway line. What happens next will echo through football history.",
                "duration": 12
            },
            {
                "title": "The Run",
                "narration": "One defender. Then two. Three. Four. Five defenders left in his wake. The ball glued to his left foot, dancing through a forest of legs. This isn't just skill. This is poetry in motion.",
                "duration": 15
            },
            {
                "title": "The Finish",
                "narration": "The goalkeeper rushes out. Messi stays calm. He slots it home. The stadium erupts. Commentators compare it to Maradona's 1986 masterpiece. But this is Messi's moment. His legacy begins here.",
                "duration": 14
            }
        ],
        "stats": [
            {"label": "Distance Covered", "value": "62m"},
            {"label": "Defenders Beaten", "value": "5"},
            {"label": "Age", "value": "19"}
        ]
    },
    
    "messi_boateng_2015": {
        "title": "The Moment of Magic",
        "subtitle": "Messi vs Bayern Munich, 2015",
        "chapters": [
            {
                "title": "The Stage",
                "narration": "Champions League semi-final. Bayern Munich. The giants of European football. One of the world's best defenders, Jerome Boateng, stands between Messi and glory.",
                "duration": 11
            },
            {
                "title": "The Move",
                "narration": "Messi receives. One touch. Boateng commits. The slightest shift of weight. A body feint so subtle, so devastating, that a world-class defender collapses to the turf. Time stands still.",
                "duration": 14
            },
            {
                "title": "The Chip",
                "narration": "Manuel Neuer rushes out. Another goalkeeper, another victim. Messi lifts it. Delicate. Precise. Unstoppable. The ball kisses the net. Barcelona advances. History is made.",
                "duration": 13
            }
        ],
        "stats": [
            {"label": "Goals That Night", "value": "2"},
            {"label": "Defenders Destroyed", "value": "∞"},
            {"label": "Legendary Status", "value": "CONFIRMED"}
        ]
    },
    
    "messi_world_cup_2022": {
        "title": "The Dream Fulfilled",
        "subtitle": "Qatar 2022",
        "chapters": [
            {
                "title": "The Journey",
                "narration": "Four World Cups. Four heartbreaks. 2006, too young. 2010, too soon. 2014, so close. 2018, the dream fading. But champions never quit. And neither does Lionel Messi.",
                "duration": 14
            },
            {
                "title": "The Tournament",
                "narration": "Qatar 2022. His last chance. He leads Argentina through the group stage. He destroys Australia. He outplays the Netherlands. He faces Croatia. Every touch matters. Every goal brings him closer.",
                "duration": 15
            },
            {
                "title": "The Final",
                "narration": "December 18th. France. Mbappé. A hat-trick thriller. Extra time. Penalties. Then, finally, the moment. Messi lifts the golden trophy. Tears flow. A career completed. A legend cemented. Forever.",
                "duration": 16
            }
        ],
        "stats": [
            {"label": "Goals in Tournament", "value": "7"},
            {"label": "Years Waiting", "value": "16"},
            {"label": "Golden Ball Awards", "value": "2"}
        ]
    },
    
    "messi_91_goals": {
        "title": "The Year of Impossibility",
        "subtitle": "2012: Breaking All Records",
        "chapters": [
            {
                "title": "The Record",
                "narration": "1972. Gerd Müller scores 85 goals in a calendar year. A record deemed unbreakable for 40 years. Untouchable. Impossible. Until 2012.",
                "duration": 11
            },
            {
                "title": "The Chase",
                "narration": "January through November. Lionel Messi is unstoppable. La Liga. Champions League. Copa del Rey. Argentina. Every competition. Every opponent. The goals keep coming. Week after week. The world watches in awe.",
                "duration": 16
            },
            {
                "title": "The Achievement",
                "narration": "December 9th, 2012. Goal number 86. The record is broken. But Messi doesn't stop. He finishes with 91. Ninety-one goals. In one year. A goal every 63 minutes. Superhuman. Unmatched. Legendary.",
                "duration": 15
            }
        ],
        "stats": [
            {"label": "Total Goals", "value": "91"},
            {"label": "Previous Record", "value": "85"},
            {"label": "Minutes Per Goal", "value": "63"}
        ]
    }
}


def get_enhanced_script(story_key):
    """Get enhanced script for a story"""
    return ENHANCED_SCRIPTS.get(story_key, None)


def get_all_story_keys():
    """Get all available story keys"""
    return list(ENHANCED_SCRIPTS.keys())
