class Restaurant:
    def __init__(
        self,
        name: str,
        image_url: str,
        home_page: str,
        id: str,
        ratings: str,
        cuisine: str,
        telephone: str,
        menu_url: str,
        address: str,
        opening_hours: dict,
    ):
        self.name = name
        self.image_url = image_url
        self.home_page = home_page
        self.id = id
        self.ratings = ratings
        self.cuisine = cuisine
        self.telephone = telephone
        self.menu_url = menu_url
        self.address = address
        self.opening_hours = opening_hours

    def __repr__(self) -> str:
        return f"Restaurant(id='{self.id}', name='{self.name}', cuisine='{self.cuisine}')"

    def __str__(self) -> str:
        return f"Restaurant ID: {self.id}, Name: {self.name}, Cuisine: {self.cuisine}"
