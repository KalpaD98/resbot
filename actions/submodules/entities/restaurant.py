class Restaurant:
    def __init__(
            self,
            id: str,
            name: str,
            ratings: str,
            cuisine: str,
            menu_url: str,
            image_url: str,
            home_page_url: str,
            telephone: str,
            address: str,
            opening_hours: dict,
    ):
        self.id = id
        self.name = name
        self.ratings = ratings
        self.cuisine = cuisine
        self.menu_url = menu_url
        self.image_url = image_url
        self.home_page = home_page_url
        self.telephone = telephone
        self.address = address
        self.opening_hours = opening_hours

    def __repr__(self) -> str:
        return f"Restaurant(id='{self.id}', name='{self.name}', cuisine='{self.cuisine}')"

    def __str__(self) -> str:
        return f"Restaurant ID: {self.id}, Name: {self.name}, Cuisine: {self.cuisine}"
