from dataclasses import dataclass
from cyclonedds.idl import IdlStruct

from cyclonedds.domain import DomainParticipant
from cyclonedds.topic import Topic
from cyclonedds.sub import DataReader
from cyclonedds.util import duration


@dataclass
class Message(IdlStruct):
    text: str


participant = DomainParticipant()
topic = Topic(participant, "Announcements", Message)
reader = DataReader(participant, topic)

for msg in reader.take_iter(timeout = duration(minutes=5)):
    print(msg.text)
