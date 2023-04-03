import datetime


def get_user_bookings(user_id: str, booking_type: str = "all"):
    # Fetch user bookings from the database (customize this part)
    user_bookings = [
        {
            "booking_id": "bid_123",
            "restaurant_id": "rtid_123",
            "restaurant_name": "Restaurant A",
            "restaurant_image": "https://example.com/imageA.jpg",
            "booking_date": "2023-06-10"
        },
        {
            "booking_id": "bid_124",
            "restaurant_id": "rtid_124",
            "restaurant_name": "The Cozy Corner",
            "restaurant_image": "https://example.com/imageB.jpg",
            "booking_date": "2023-05-15"
        },
        {
            "booking_id": "bid_125",
            "restaurant_id": "rtid_125",
            "restaurant_name": "The Italian Bistro",
            "restaurant_image": "https://example.com/imageC.jpg",
            "booking_date": "2023-07-20"
        },
        {
            "booking_id": "bid_126",
            "restaurant_id": "rtid_126",
            "restaurant_name": "The Sushi Spot",
            "restaurant_image": "https://example.com/imageD.jpg",
            "booking_date": "2023-08-05"
        },
        {
            "booking_id": "bid_127",
            "restaurant_id": "rtid_127",
            "restaurant_name": "The Burger Bar",
            "restaurant_image": "https://example.com/imageE.jpg",
            "booking_date": "2023-04-30"
        },
        {
            "booking_id": "bid_128",
            "restaurant_id": "rtid_128",
            "restaurant_name": "The Vegan Café",
            "restaurant_image": "https://example.com/imageF.jpg",
            "booking_date": "2023-09-12"
        }
    ]

    # Get today's date
    today = datetime.datetime.now().date()

    # Filter bookings based on the booking_type
    if booking_type == "past":
        user_bookings = [booking for booking in user_bookings if
                         datetime.datetime.strptime(booking["booking_date"], "%Y-%m-%d").date() < today]
    elif booking_type == "upcoming":
        user_bookings = [booking for booking in user_bookings if
                         datetime.datetime.strptime(booking["booking_date"], "%Y-%m-%d").date() >= today]

    return user_bookings
