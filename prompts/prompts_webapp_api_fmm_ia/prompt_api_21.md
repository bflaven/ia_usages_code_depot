# prompt_api_20.md

## prompt
As an advanced programmer in Python, with FastAPI, create a endpoint where you add a real json example in "Example Value" in the swagger documentation.


I do not see the sample "Item.schema_extra" in the swagger documentation? How do you call it and show in the doc?



How do you load a json example inside the field "Request body" when you click on the button "Try it out"

{
  "text": "string"
}


## output

I apologize for the confusion. It seems I made a mistake. FastAPI's `@app.post` decorator doesn't directly support an `example` argument for specifying example values in the Swagger documentation.

Instead, you can provide examples using Pydantic's `schema_extra` attribute. Here's how you can do it:

```python
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str = None
    price: float
    tax: float = None

@app.post("/items/", response_model=Item, summary="Create an item", response_description="The created item")
async def create_item(item: Item):
    return item

# Provide examples using Pydantic's schema_extra attribute
Item.schema_extra = {
    "example": {
        "name": "Example Item",
        "description": "This is an example item",
        "price": 99.99,
        "tax": 9.99
    }
}
```

In the code above, we attach the example directly to the `Item` class using the `schema_extra` attribute. This will be reflected in the Swagger documentation.

Now, when you navigate to `http://localhost:8000/docs`, you should see the Swagger UI documentation with the example JSON provided for the `Item` model.
