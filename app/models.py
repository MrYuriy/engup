from app import db

class Language(db.Model):
    __tablename__ = 'languages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64), unique=True, nullable=False)
    words = db.relationship('Word', backref='language', lazy='joined')


class Word(db.Model):
    __tablename__ = 'words'

    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(128), nullable=False)
    language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)
    translations = db.relationship('Translation', back_populates='word', lazy='subquery')


class Translation(db.Model):
    __tablename__ = 'translations'

    id = db.Column(db.Integer, primary_key=True)
    word_id = db.Column(db.Integer, db.ForeignKey('words.id'), nullable=False)
    target_language_id = db.Column(db.Integer, db.ForeignKey('languages.id'), nullable=False)
    translation_text = db.Column(db.String(128), nullable=False)
    
    word = db.relationship('Word', back_populates='translations', lazy='joined')
    target_language = db.relationship('Language', foreign_keys=[target_language_id], lazy='joined')

    __table_args__ = (db.UniqueConstraint('word_id', 'target_language_id', name='unique_word_translation'),)


class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    native_language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))
    learning_language_id = db.Column(db.Integer, db.ForeignKey('languages.id'))

    native_language = db.relationship('Language', foreign_keys=[native_language_id], lazy='joined')
    learning_language = db.relationship('Language', foreign_keys=[learning_language_id], lazy='joined')


class UserTranslations(db.Model):
    __tablename__ = 'usertranslations'

    id = db.Column(db.Integer, primary_key=True)
    status = db.Column(db.Integer, default=0)
    translation_id = db.Column(db.Integer, db.ForeignKey('translations.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    user = db.relationship('User', backref='user_translations', lazy='joined')
    translation = db.relationship('Translation', backref='user_translations', lazy='joined')


    __table_args__ = (db.UniqueConstraint('user_id', 'translation_id', name='unique_user_translation'),)


