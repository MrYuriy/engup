from app import create_app, db
from app.models import Language, Word, Translation
import json

def create_mock_translation():
    # Check if languages already exist
    english = Language(name="English")
    ukranian = Language(name="Ukranian")
    db.session.add_all([english, ukranian])
    db.session.commit()
    
    with open('utils\\moc_eng_ukr_dictionary.json', 'r', encoding="utf-8") as file:
        eng_ua_dict = json.load(file)
    
    translation_data = []

    for eng, ua in eng_ua_dict.items():
        eng_word = Word(text=eng, language=english)
        ua_word = Word(text=ua, language=ukranian)
        translation_data.append((eng_word, ua_word))
    
    db.session.add_all(list(sum(translation_data, ())))
    db.session.commit()
    
    translation_instances = []
    for eng_word, ukr_word in translation_data:
        translation = Translation(
            word=eng_word,
            target_language=ukranian,
            translation_text=ukr_word.text
        )
        translation_instances.append(translation)
    
    db.session.add_all(translation_instances)
    db.session.commit()


