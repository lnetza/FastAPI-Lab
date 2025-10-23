from typing import Optional
from enum import Enum
from pydantic import BaseModel
from pydantic import Field
from pydantic import EmailStr
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

#Enums
class HairColor(Enum):
    white = "white"
    brown = "brown"
    black = "black"
    blonde = "blonde"
    red = "red"

#Models
class Location(BaseModel):
    city: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    state: str = Field(
        ...,
        min_length=1,
        max_length=50

    )
    country: str = Field(
        ...,
        min_length=1,
        max_length=50
        )

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50
        )
    email: Optional[EmailStr] = Field(default=None)
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)

@app.get("/")
def home():
    return {"url": "https://www.google.com"}

@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

#Validaciones: Query parameters
@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1, 
        max_length=50,
        title="Person Name",
        description="This is the person name. It's between 1 and 50 characters"
        ),
    age: str = Query(
        ...,
        title="Person Age",
        description="This is the person age. It's required"
        )
):
    return {name: age}

#Validaciones: Path parameters
@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ...,
        gt=0,
        title="Person ID",
        description="This is the person ID. It's required and must be greater than 0"
        )
):
    return {person_id: "It exists!"}

#Validaciones: Request Body
@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID",
        gt=0,
    ),
    person: Person = Body(...),
    location: Location = Body(...)
):
    results = person.dict()
    results.update(location.dict())
    return results

