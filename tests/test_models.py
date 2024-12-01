import pytest
from app import create_app, db
from app.models import Language, Word, Translation, User, UserTranslations

@pytest.fixture
def app():
    app = create_app("config.TestingConfig")  # Використовуйте конфігурацію для тестування
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def init_database(app):
    # Додавання мов
    english = Language(name="English")
    spanish = Language(name="Spanish")
    db.session.add_all([english, spanish])
    db.session.commit()

    # Додавання слів
    word_hello = Word(text="hello", language=english)
    word_hola = Word(text="hola", language=spanish)
    db.session.add_all([word_hello, word_hola])
    db.session.commit()

    # Додавання перекладу
    translation = Translation(
        word=word_hello,
        target_language=spanish,
        translation_text="hola"
    )
    db.session.add(translation)
    db.session.commit()

    # Додавання користувача
    user = User(username="test_user", password="hashed_password", native_language=english, learning_language=spanish)
    db.session.add(user)
    db.session.commit()

    # Додавання статусу перекладу для користувача
    user_translation = UserTranslations(status=1, translation_id=translation.id, user_id=user.id)
    db.session.add(user_translation)
    db.session.commit()

    return {
        "languages": [english, spanish],
        "words": [word_hello, word_hola],
        "translations": [translation],
        "users": [user],
        "user_translations": [user_translation]
    }


def test_language_model(init_database):
    languages = Language.query.all()
    assert len(languages) == 2
    assert languages[0].name == "English"
    assert languages[1].name == "Spanish"

def test_word_model(init_database):
    words = Word.query.all()
    assert len(words) == 2
    assert words[0].text == "hello"
    assert words[1].text == "hola"
    assert words[0].language.name == "English"

def test_translation_model(init_database):
    translations = Translation.query.all()
    assert len(translations) == 1
    assert translations[0].word.text == "hello"
    assert translations[0].translation_text == "hola"
    assert translations[0].word.language.name == "English"
    assert translations[0].target_language.name == "Spanish"

def test_user_model(init_database):
    users = User.query.all()
    assert len(users) == 1
    user = users[0]
    assert user.username == "test_user"
    assert user.native_language.name == "English"
    assert user.learning_language.name == "Spanish"

def test_user_translations_model(init_database):
    user_translations = UserTranslations.query.all()
    assert len(user_translations) == 1
    user_translation = user_translations[0]
    assert user_translation.status == 1
    assert user_translation.user.username == "test_user"
    assert user_translation.translation.translation_text == "hola"
