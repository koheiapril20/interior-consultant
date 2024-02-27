from langchain.pydantic_v1 import BaseModel, Field
from typing import Optional

class BaseRoom(BaseModel):
    size: Optional[str] = Field(
        description="rough room size",
        examples=['4x6 square meters', '6 tatami mats']
    )
    structure: Optional[str] = Field(
        description="room's structure",
        examples=['a large window on one wall']
    )
    usage: Optional[str] = Field(
        description="what this room is for",
        examples=["living room", "bed room", "home office", "children's room"],
    )
    wall_texture: Optional[str] = Field(
        description="characteristics of the walls",
        examples=["white wallpaper", "gloss", "concrete"],
    )
    floor_texture: Optional[str] = Field(
        description="characteristics of the floor",
        examples=["light brown natural wood", "linoleum", "tatami", "dark grey carpet"],
    )

class Furniture(BaseModel):
    name: str = Field(
        description="name of furniture in English",
        examples=['couch', 'dining table', 'low table', 'lamp'],
    )
    characteristics: Optional[list[str]] = Field(
        description='detailed characteristics of the furniture in English',
        examples=[['wooden', 'round', '1-meter height']],
    )

class InteriorPlan(BaseModel):
    base_room: Optional[BaseRoom]
    interior_style: Optional[str] = Field(
        description="preffered interior style in English",
        examples=["mid-century", "industrial", "scandinavian", "bohemian", "urban modern", "chic", "Japanese zen", 'natural-style interior with the warmth of wood'],
    )
    theme_colors : Optional[list[str]] = Field(
        description="interior theme color combination",
        examples=[["purple", "white"], ["monochrome"]],
    )
    accent_color: Optional[str] = Field(
        description="color that gives accent to the room",
        examples=["red", "orange", "blue"],
    )
    furniture: Optional[list[Furniture]]

class SimilarProductQuery(BaseModel):
    keyword: str = Field(
        description="which item the user wants to search for",
        examples=['couch', 'dining table', 'low table', 'lamp'],
    )
    image_url: str = Field(
        description="URL of the previous generated image. This must include accurate query parameters",
        examples=['https://oaidalleapiprodscus.blob.core.windows.net/private/org-mqlsaZdQf6xEf7Dyvh4URc1j/user-ZDCWvYtHfmkhqYPZfMSgIsV6/img-lhIvrXNS4HVaw2ls14TAGhI7.png?st=2024-02-27T03%3A24%3A30Z&se=2024-02-27T05%3A24%3A30Z&sp=r&sv=2021-08-06&sr=b&rscd=inline&rsct=image/png&skoid=6aaadede-4fb3-4698-a8f6-684d7786b067&sktid=a48cca56-e6da-484e-a814-9c849652bcb3&skt=2024-02-27T03%3A07%3A04Z&ske=2024-02-28T03%3A07%3A04Z&sks=b&skv=2021-08-06&sig=29SjGL2GTofAyQDge5ywYPt8o%2BXYC5%2B1YVthMf3t7Z4%3D'],
    )

class AskPreferenceContext(BaseModel):
    plan: InteriorPlan

class GenerateImageContext(BaseModel):
    plan: InteriorPlan

class SearchSimilarProductsContext(BaseModel):
    query: SimilarProductQuery
