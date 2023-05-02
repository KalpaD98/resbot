from typing import List, Optional

from bson.objectid import ObjectId


class Restaurant:
    ID = "id"
    BUSINESS_ID = "business_id"
    NAME = "name"
    CITY = "city"
    STATE = "state"
    POSTAL_CODE = "postal_code"
    ADDRESS = "address"
    LATITUDE = "latitude"
    LONGITUDE = "longitude"
    CUISINE = "cuisine"
    RATINGS = "ratings"
    OPENING_HOURS = "opening_hours"
    IMAGE_URL = "image_url"
    HOME_PAGE_URL = "home_page_url"
    MENU_URL = "menu_url"
    CATEGORIES = "categories"
    MON_TO_FRI = "Mon - Fri"
    SAT_SUN = "Sat, Sun"
    REVIEW_COUNT = "review_count"

    def __init__(
            self,
            name: str,
            ratings: str,
            cuisine: str,
            menu_url: str,
            image_url: str,
            home_page_url: str,
            address: str,
            opening_hours: dict,
            city: Optional[str] = None,
            state: Optional[str] = None,
            postal_code: Optional[str] = None,
            latitude: Optional[float] = None,
            longitude: Optional[float] = None,
            categories: Optional[List[str]] = None,
            business_id: Optional[str] = None,
            review_count: Optional[int] = None,
            id=None,
    ):
        self.id = f"rid_{ObjectId()}" if id is None else id
        self.business_id = business_id
        self.name = name
        self.ratings = ratings
        self.cuisine = cuisine
        self.menu_url = menu_url
        self.image_url = image_url
        self.home_page = home_page_url
        self.address = address
        self.city = city
        self.state = state
        self.postal_code = postal_code
        self.latitude = latitude
        self.longitude = longitude
        self.opening_hours = opening_hours
        self.categories = categories
        self.review_count = review_count

    def __repr__(self) -> str:
        return f"Restaurant(id='{self.id}', name='{self.name}', cuisine='{self.cuisine}')"

    def __str__(self) -> str:
        return f"Restaurant ID: {self.id}, Name: {self.name}, Cuisine: {self.cuisine}"

    def to_dict(self):
        return {
            self.ID: self.id,
            self.BUSINESS_ID: self.business_id,
            self.NAME: self.name,
            self.RATINGS: self.ratings,
            self.CUISINE: self.cuisine,
            self.MENU_URL: self.menu_url,
            self.IMAGE_URL: self.image_url,
            self.HOME_PAGE_URL: self.home_page,
            self.ADDRESS: self.address,
            self.CITY: self.city,
            self.STATE: self.state,
            self.POSTAL_CODE: self.postal_code,
            self.LATITUDE: self.latitude,
            self.LONGITUDE: self.longitude,
            self.OPENING_HOURS: self.opening_hours,
            self.CATEGORIES: self.categories,
            self.REVIEW_COUNT: self.review_count
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            name=data[cls.NAME],
            ratings=data[cls.RATINGS],
            cuisine=data[cls.CUISINE],
            menu_url=data[cls.MENU_URL],
            image_url=data[cls.IMAGE_URL],
            home_page_url=data[cls.HOME_PAGE_URL],
            address=data[cls.ADDRESS],
            city=data[cls.CITY],
            state=data[cls.STATE],
            postal_code=data[cls.POSTAL_CODE],
            latitude=data[cls.LATITUDE],
            longitude=data[cls.LONGITUDE],
            opening_hours=data[cls.OPENING_HOURS],
            categories=data[cls.CATEGORIES],
            business_id=data[cls.BUSINESS_ID],  # Pass the business_id attribute
            id=data[cls.ID],  # Pass the id attribute
            review_count=data[cls.REVIEW_COUNT],
        )
