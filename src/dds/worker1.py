from dataclasses import dataclass
from cyclonedds.idl import IdlStruct

from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.pub import DataWriter

@dataclass
class Message(IdlStruct):
    text: str

message = Message(text=f"Hello, World!")


participant = DomainParticipant()
topic = Topic(participant, "Announcements", Message)
writer = DataWriter(participant, topic)

writer.write(message)