from pydantic import BaseModel, Field
import motor.motor_asyncio


class TasksDB:
    def __init__(self):
        self.client = None
        self.db = None
        self.collection = None

    async def connect(self):
        self.client = motor.motor_asyncio.AsyncIOMotorClient('localhost', 27017)
        self.db = self.client['TasksDB']
        self.collection = self.db.get_collection("tasks_collection")

    async def disconnect(self):
        self.client.close()

    @staticmethod
    def serialize(task):
        return {"title": task["title"],
                "description": task["description"],
                "statue": task["status"]}


class Task(BaseModel):
    title: str = Field(max_length=32, uniques=True)
    description: str = Field(max_length=200)
    status: bool = Field(default=False)
