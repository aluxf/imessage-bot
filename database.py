from peewee import *

# Define the database
db = SqliteDatabase('database.db')

# Define the base model class
class BaseModel(Model):
    class Meta:
        database = db

class ChatRoom(BaseModel):
    name = CharField(unique=True, primary_key=True)

class ChatUser(BaseModel):
    name = CharField()
    phone_number = CharField()
    chatroom = ForeignKeyField(ChatRoom, backref='chatusers')
    class Meta:
        indexes = (
            # Create a unique index on name/chatroom
            (('name', 'chatroom'), True),
            (('phone_number', 'chatroom'), True),
        )

#initialize database
db.connect()
db.create_tables([
    ChatRoom, 
    ChatUser
])
db.close()
