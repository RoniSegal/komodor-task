SAMPLE_PAYLOAD = {
    "order_id": "ord-8821",
    "city": "Tel Aviv",
    "signals": [
        {
            "source": "order_tracker",
            "message": "Order stuck in 'restaurant_accepted' state for 23 minutes. Expected max: 5 minutes.",
        },
        {
            "source": "driver_dispatch",
            "message": "3 consecutive driver assignment attempts failed. Last failure reason: no_drivers_nearby.",
        },
        {
            "source": "restaurant_health",
            "message": "Pasta Palace (id: rest-441) has had 7 orders cancelled in the last 15 minutes. Average prep time today: 34 min vs. 12 min baseline.",
        },
        {
            "source": "customer_support",
            "message": "Customer contacted support: 'Where is my food? It's been 40 minutes.'",
        },
    ],
}
