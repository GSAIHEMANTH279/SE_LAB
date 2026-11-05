
"""Manage parcel bookings, tracking, delivery status, and shipping costs."""

import secrets
import tempfile
from datetime import date

STATUS_FLOW = [
    "Booked",
    "Picked Up",
    "In Transit",
    "Out for Delivery",
    "Delivered",
]

parcels = {}


def book_parcel(sender, receiver, weight_kg, history=None):
    """Book a parcel and return its tracking ID."""
    if history is None:
        history = []

    tracking_id = f"TRK{10001 + len(parcels)}"

    parcels[tracking_id] = {
        "sender": sender,
        "receiver": receiver,
        "weight": weight_kg,
        "status": 0,
        "booked": str(date.today()),
    }

    history.append(tracking_id)
    return tracking_id


def advance_status(tracking_id):
    """Advance a parcel to its next status, if possible."""
    parcel = parcels[tracking_id]

    if parcel["status"] < len(STATUS_FLOW) - 1:
        parcel["status"] += 1

    return STATUS_FLOW[parcel["status"]]


def shipping_cost(weight_kg):
    """Calculate shipping cost based on parcel weight in kilograms."""
    cost = 50

    if weight_kg > 1:
        cost += (weight_kg - 1) * 30

    return round(cost, 2)


def track_parcel(tracking_id):
    """Return a parcel's route and current status."""
    parcel = parcels.get(tracking_id)

    if parcel is None:
        return f"Unknown tracking id {tracking_id}"

    route = f"{parcel['sender']} -> {parcel['receiver']}"
    status = STATUS_FLOW[parcel["status"]]

    return f"{route}: {status}"


def is_with_courier(tracking_id):
    """Check whether a parcel has been picked up or is in transit."""
    parcel = parcels.get(tracking_id)

    if parcel is None:
        return False

    status = STATUS_FLOW[parcel["status"]]
    return status in ("Picked Up", "In Transit")


def label_path():
    """Create a secure temporary file and return its path."""
    with tempfile.NamedTemporaryFile(
        suffix=".txt",
        delete=False,
    ) as temporary_file:
        return temporary_file.name


def main():
    """Run the parcel-tracking demonstration."""
    first = book_parcel("Bengaluru Books", "Ravi Kumar", 2.5)
    second = book_parcel("Gadget Hub", "Sneha Rao", 0.8)
    third = book_parcel("Spice Store", "Imran Khan", 4)

    advance_status(first)
    advance_status(first)
    advance_status(second)

    for _ in range(6):
        advance_status(third)

    for tracking_id in (first, second, third):
        print(track_parcel(tracking_id))
        print("  with courier:", is_with_courier(tracking_id))
        print("  cost:", shipping_cost(parcels[tracking_id]["weight"]))

    print(track_parcel("TRK00000"))

    delivery_otp = secrets.randbelow(9000) + 1000
    print("Delivery OTP for", third, "is", delivery_otp)
    print("Parcels booked today:", len(parcels))


if __name__ == "__main__":
    main()
